from rest_framework.serializers import ModelSerializer
from .models import Course, Lesson


class CourseSerializer(ModelSerializer):
    """Сериализатор для курсов"""

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    """Сериализатор для уроков"""

    class Meta:
        model = Lesson
        fields = "__all__"
