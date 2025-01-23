from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from users.models import User


@shared_task
def user_deactivator():
    """Деактивация пользователей, которые не заходили более месяца"""

    users = User.objects.filter(last_login__lt=now() - timedelta(days=30))
    if users.count() > 0:
        users.update(is_active=False)
        users.save()
