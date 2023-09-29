from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model


class UserSerializer(ModelSerializer):
    """
    Сериализатор для модели пользователей.
    """
    class Meta:
        model = get_user_model()
        fields = ["username", "password", "photo", "email", "first_name",
                  "last_name", "bio", "notifications"]
        extra_kwargs = {"password": {"write_only": True}}
