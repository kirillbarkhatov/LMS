from django.shortcuts import get_object_or_404
from rest_framework import generics, views, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsModer, IsOwner

from .models import Course, CourseSubscription, Lesson
from .paginators import TwoItemsPaginator
from .serializers import (CoursePaymentSerializer, CourseSerializer,
                          CourseSubscriptionSerializer, LessonSerializer)
from .services import (create_stipe_price,
                       create_stripe_session)
from .tasks import send_mail_course_update


class CourseViewSet(viewsets.ModelViewSet):
    """Вьюсет для курсов"""

    model = Course
    serializer_class = CourseSerializer
    pagination_class = TwoItemsPaginator

    def get_queryset(self):
        """Фильтруем набор данных в зависимости от пользователя"""

        if self.request.user.groups.filter(name="Модератор").exists():
            return Course.objects.all()
        user = self.request.user
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """Устанавливает права на действия пользователя."""

        if self.action in (
            "list",
            "retrieve",
            "update",
            "partial_update",
        ):
            permission_classes = [IsAuthenticated, IsModer | IsOwner]
        elif self.action in ("create",):
            permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action in ("destroy",):
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_update(self, serializer):
        course_id = self.kwargs.get("pk")
        send_mail_course_update.delay(course_id)
        # course = get_object_or_404(Course, id=course_id)
        # subscriptions = course.course_subscription.all()
        #
        # # Преобразуем в список словарей
        # subs_data = [sub.user.email
        #              for sub in subscriptions
        #              ]
        # print(subs_data)
        serializer.save()


class LessonCreateApiView(generics.CreateAPIView):
    """Создание урока"""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListApiView(generics.ListAPIView):
    """Список уроков"""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]
    pagination_class = TwoItemsPaginator

    def get_queryset(self):
        """Фильтруем набор данных в зависимости от пользователя"""

        if self.request.user.groups.filter(name="Модератор").exists():
            return Lesson.objects.all()
        user = self.request.user
        return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Получить один урок"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Обновить урок"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удалить урок"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class CourseSubscriptionApiView(views.APIView):
    """Подписка на курс"""

    serializer_class = CourseSubscriptionSerializer
    queryset = CourseSubscription.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        user = self.request.user
        course_id = self.request.data.get("course")
        course = get_object_or_404(Course, id=course_id)

        subs_item = self.queryset.filter(user=user, course=course)

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            CourseSubscription.objects.create(user=user, course=course)
            message = "подписка добавлена"

        return Response({"message": message})


class CoursePaymentCreateApiView(generics.CreateAPIView):
    """Оплата за курс"""

    serializer_class = CoursePaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        course_id = self.request.data.get("course")
        course = get_object_or_404(Course, id=course_id)
        amount_in_usd = course.price
        payment = serializer.save(amount=amount_in_usd)
        # amount_in_usd = convert_rub_to_usd(100)
        price = create_stipe_price(amount_in_usd, course.name)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()
