from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    """
    Настройка формы для регистрации с изменениями в HTML форме.
    """
    class Meta:
        model = CustomUser
        fields = (
            "username", "password1", "password2", "photo", "email",
            "first_name", "last_name", "bio", "notifications"
        )


class CustomUserChangeForm(UserChangeForm):
    """
    Настройка формы редактирования полей пользователя.
    """
    class Meta:
        model = CustomUser
        fields = (
            "username", "photo", "email", "first_name", "last_name", "bio",
            "notifications"
        )
