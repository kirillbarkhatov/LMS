from rest_framework.routers import SimpleRouter
from django.urls import path

from .views import CourseViewSet, LessonListApiView, LessonDestroyAPIView, LessonCreateApiView, LessonRetrieveAPIView, LessonUpdateAPIView
from .apps import LmsConfig


app_name = LmsConfig.name

router = SimpleRouter()
router.register("course", CourseViewSet)

urlpatterns = [
    path("lesson/", LessonListApiView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>", LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
    path("lesson/create", LessonCreateApiView.as_view(), name="lesson_create"),
    path("lesson/<int:pk>/update", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lesson/<int:pk>/delete", LessonDestroyAPIView.as_view(), name="lesson_delete"),
]

urlpatterns += router.urls
