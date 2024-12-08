from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Course, Lesson


class CourseSerializer(ModelSerializer):
    """Сериализатор для курсов"""

    lessons_count = SerializerMethodField()

    def get_lessons_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    """Сериализатор для уроков"""

    class Meta:
        model = Lesson
        fields = "__all__"
