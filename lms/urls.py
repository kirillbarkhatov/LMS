from django.urls import path
from rest_framework.routers import DefaultRouter

from .apps import LmsConfig
from .views import (CourseSubscriptionApiView, CourseViewSet,
                    LessonCreateApiView, LessonDestroyAPIView,
                    LessonListApiView, LessonRetrieveAPIView,
                    LessonUpdateAPIView)

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r"course", CourseViewSet, basename="course")

urlpatterns = [
    path("lesson/", LessonListApiView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>", LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
    path("lesson/create", LessonCreateApiView.as_view(), name="lesson_create"),
    path("lesson/<int:pk>/update", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path(
        "lesson/<int:pk>/delete", LessonDestroyAPIView.as_view(), name="lesson_delete"
    ),
    path(
        "course/subscribe", CourseSubscriptionApiView.as_view(), name="course_subscribe"
    ),
]

urlpatterns += router.urls
