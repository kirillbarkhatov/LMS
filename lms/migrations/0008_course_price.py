# Generated by Django 5.1.3 on 2024-12-22 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0007_coursepayment"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="price",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=10, verbose_name="Цена в рублях"
            ),
        ),
    ]
