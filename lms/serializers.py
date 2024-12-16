from rest_framework import serializers

from .models import Course, Lesson
from .validators import validate_lesson_url


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков"""

    url = serializers.URLField(validators=[validate_lesson_url])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курсов"""

    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = "__all__"
