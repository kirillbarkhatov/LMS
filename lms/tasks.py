from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from lms.models import Course
from config.settings import DEFAULT_FROM_EMAIL


@shared_task
def send_mail_course_update(course_id):
    print("Hello")
    course = get_object_or_404(Course, id=course_id)
    subscriptions = course.course_subscription.all()

    # Преобразуем в список словарей
    recipient_list = [sub.user.email
                 for sub in subscriptions
                 ]
    # recipient_list.append(DEFAULT_FROM_EMAIL)
    print(recipient_list)

    # self.object = self.get_object()
    # # Получите данные, которые хотите отправить
    subject = f"Курс {course.name} обновлен!"
    message = f'Здравствуйте! Сообщаем, что в курсе "{course.name}" обновления!'
    # # self.object.status = "running"
    # # self.object.save()
    from_email = DEFAULT_FROM_EMAIL
    # recipient_list = [
    #     recipient.email for recipient in self.object.recipients.all()
    # ]  # Укажите адреса получателей
    #
    # Отправка письма
    responses = {}

    for recipient in recipient_list:
        try:
            send_mail(subject, message, from_email, [recipient])

            responses[recipient] = "Успешно отправлено"
        except Exception as e:
            response = f"{recipient}: Ошибка: {str(e)}"
            responses[recipient] = f"Ошибка: {str(e)}"

    print(responses)