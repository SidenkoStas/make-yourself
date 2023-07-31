from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username", "photo", "email", "first_name", "last_name", "bio",
            "notifications"
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "username", "photo", "email", "first_name", "last_name", "bio",
            "notifications"
        )
