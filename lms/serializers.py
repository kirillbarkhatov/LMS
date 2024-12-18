from rest_framework import serializers

from .models import Course, Lesson, CourseSubscription
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
    subscription = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, course):
        return course.lessons.count()

    def get_subscription(self, course):
        return course.course_subscription.exists()

    class Meta:
        model = Course
        fields = "__all__"


class CourseSubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки на курс"""

    class Meta:
        model = CourseSubscription
        fields = ["course"]

