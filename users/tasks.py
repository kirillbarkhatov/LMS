from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from users.models import User
from config.settings import DEFAULT_FROM_EMAIL


@shared_task
def user_deactivator():
    users = User.objects.filter(last_login__lt=now() - timedelta(days=30))
    users.update(is_active=False)
    users.save()
