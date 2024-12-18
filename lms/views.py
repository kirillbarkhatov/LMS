from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsModer, IsOwner

from .models import Course, Lesson, CourseSubscription
from .paginators import TwoItemsPaginator
from .serializers import CourseSerializer, LessonSerializer, CourseSubscriptionSerializer


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


class CourseSubscriptionApiView(generics.CreateAPIView):
    """Подписка на курс"""

    serializer_class = CourseSubscriptionSerializer
    queryset = CourseSubscription.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # return self.create(request, *args, **kwargs)

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
