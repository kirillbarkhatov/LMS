# Generated by Django 5.1.3 on 2024-12-22 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0012_alter_course_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="price",
            field=models.PositiveIntegerField(
                default=100, verbose_name="Цена в долларах США"
            ),
        ),
    ]
