from rest_framework import serializers


def validate_lesson_url(value):
    """Валидатор ссылок на уроки"""

    if "youtube.com" not in value:
        raise serializers.ValidationError("Допускаются только ссылки на youtube.com")
