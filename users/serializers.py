from rest_framework.serializers import ModelSerializer
from .models import User


class UserSerializer(ModelSerializer):
    """Сериализатор для пользователя"""

    class Meta:
        model = User
        fields = "__all__"