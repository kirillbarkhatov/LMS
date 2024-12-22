from rest_framework import serializers

from .models import Course, CourseSubscription, Lesson, CoursePayment
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
        current_user = self.context.get('request', None).user
        return course.course_subscription.filter(user=current_user).exists()

    class Meta:
        model = Course
        fields = "__all__"


class CourseSubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки на курс"""

    class Meta:
        model = CourseSubscription
        fields = ["course"]


class CoursePaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для оплаты курсов"""

    class Meta:
        model = CoursePayment
        fields = "__all__"
