from rest_framework.serializers import ModelSerializer

from .models import Payment, User


class PaymentSerializer(ModelSerializer):
    """Сериализатор для платежей"""

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    """Сериализатор для пользователя"""

    payments = PaymentSerializer(many=True)

    class Meta:
        model = User
        fields = "__all__"
