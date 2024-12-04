from django.db import models


class Course(models.Model):
    """Модель для курса"""

    name = models.CharField(max_length=50, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="lms/course", blank=True, null=True, verbose_name="Превью курса"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание курса")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Модель для уроков"""

    name = models.CharField(max_length=50, verbose_name="Название урока")
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="lessons",
        verbose_name="Курсл",
    )
    preview = models.ImageField(
        upload_to="lms/course", blank=True, null=True, verbose_name="Превью урока"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание урока")
    url = models.CharField(max_length=300, verbose_name="Ссылка на видео")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
