# Generated by Django 5.1.3 on 2024-12-18 18:45

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0004_courseenrollment"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name="CourseEnrollment",
            new_name="CourseSubscription",
        ),
    ]
