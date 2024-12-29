from django.conf import settings
from django.db import models

from config.settings import AUTH_USER_MODEL


class Course(models.Model):
    """Модель для курса"""

    name = models.CharField(max_length=50, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="lms/course", blank=True, null=True, verbose_name="Превью курса"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание курса")
    price = models.PositiveIntegerField(default=100, verbose_name="Цена в долларах США")
    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Модель для уроков"""

    name = models.CharField(max_length=50, verbose_name="Название урока")
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="lessons",
        verbose_name="Курс",
    )
    preview = models.ImageField(
        upload_to="lms/course", blank=True, null=True, verbose_name="Превью урока"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание урока")
    url = models.URLField(max_length=300, verbose_name="Ссылка на видео")
    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class CourseSubscription(models.Model):
    """Модель подписки на курс"""

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_course_subscription",
        verbose_name="Пользователь",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="course_subscription",
        verbose_name="Курс",
    )

    def __str__(self):
        return f"{self.user.email} - {self.course.name}"

    class Meta:
        verbose_name = "Подписка на курс"
        verbose_name_plural = "Подписки на курсы"


class CoursePayment(models.Model):
    """Модель для оплаты курсов"""

    amount = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Сумма оплаты"
    )
    session_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="ID сессии"
    )
    link = models.URLField(
        max_length=400, blank=True, null=True, verbose_name="Ссылка на оплату"
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="user_course_payments",
        verbose_name="Пользователь",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="course_payments",
        verbose_name="Курс",
    )

    def __str__(self):
        return self.amount

    class Meta:
        verbose_name = "Оплата за курс"
        verbose_name_plural = "Оплаты за курсы"
