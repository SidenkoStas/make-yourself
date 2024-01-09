from rest_framework.serializers import (ModelSerializer, ValidationError,
                                        CharField)
from django.contrib.auth import get_user_model


class UserSerializer(ModelSerializer):
    """
    Сериализатор для модели пользователей.
    """
    username = CharField(max_length=150)

    def validate_username(self, username):
        """
        Validate username. First char needs to be letter.
        """
        if not username[0].isalpha():
            raise ValidationError("Username is not allowed."
                                  "First char needs to be letter.")
        return username

    class Meta:
        model = get_user_model()
        fields = ["username", "password", "photo", "email", "first_name",
                  "last_name", "bio", "notifications"]
        extra_kwargs = {"password": {"write_only": True}}
