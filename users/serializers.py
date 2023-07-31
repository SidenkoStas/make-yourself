from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model


class UserSerializers(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username", "photo", "email", "first_name", "last_name",
                  "bio", "notifications"]
