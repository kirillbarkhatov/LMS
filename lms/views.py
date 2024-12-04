from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """Вьюсет для курсов"""

    model = Course
    serializer_class = CourseSerializer


class LessonCreateApiView(generics.CreateAPIView):
    """Создание урока"""

    serializer_class = LessonSerializer


class LessonListApiView(generics.ListAPIView):
    """Список уроков"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Получить один урок"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Обновить урок"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удалить урок"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
