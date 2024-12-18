from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from lms.models import Course, Lesson, CourseSubscription

class LessonTestCase(APITestCase):
    def setUp(self):
        # Подготовка данных перед каждым тестом

        self.user = User.objects.create(
            email="test1@test1.ru",
        )
        self.course = Course.objects.create(name="Геометрия", owner=self.user)
        self.lesson = Lesson.objects.create(name="Урок 1", course=self.course, url="https://www.youtube.com", owner=self.user)
        self.course_subscription = CourseSubscription(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_lesson_list(self):
        url = reverse("lms:lesson_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "url": "https://www.youtube.com",
                    "name": "Урок 1",
                    "preview": None,
                    "description": None,
                    "course": self.course.pk,
                    "owner": self.user.pk
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_lesson_retrieve(self):
        url = reverse("lms:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        url = reverse("lms:lesson_create")
        data = {
            "name": "Изо",
            "url": "https://www.youtube.com",
            "owner": self.user.pk
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("lms:lesson_update", args=(self.lesson.pk,))
        data = {
            "name": "Математика"
        }
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Математика")

    def test_lesson_delete(self):
        url = reverse("lms:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)


class CourseSubscriptionTestCase(APITestCase):
    def setUp(self):
        # Подготовка данных перед каждым тестом

        self.user = User.objects.create(
            email="test1@test1.ru",
        )
        self.course = Course.objects.create(name="Геометрия", owner=self.user)
        self.lesson = Lesson.objects.create(name="Урок 1", course=self.course, url="https://www.youtube.com",
                                            owner=self.user)
        self.course_subscription = CourseSubscription(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_course_subscribe(self):
        url = reverse("lms:course_subscribe")
        data = {
            "course": self.course.pk
        }
        response = self.client.post(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["message"], "подписка добавлена")

    #
    # def test_get(self):
    #     # Тестирование GET-запроса к API
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_post(self):
    #     # Тестирование POST-запроса к API
    #     response = self.client.post(self.url, self.data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # path("lesson/", LessonListApiView.as_view(), name="lesson_list"),
        # path("lesson/<int:pk>", LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
        # path("lesson/create", LessonCreateApiView.as_view(), name="lesson_create"),
        # path("lesson/<int:pk>/update", LessonUpdateAPIView.as_view(), name="lesson_update"),
        # path(
        #     "lesson/<int:pk>/delete", LessonDestroyAPIView.as_view(), name="lesson_delete"
        # ),
        # path("course/subscribe", CourseSubscriptionApiView.as_view(), name="course_subscribe")