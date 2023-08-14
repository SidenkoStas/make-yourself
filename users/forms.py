from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import EmailField


class CustomUserCreationForm(UserCreationForm):
    # email = EmailField(max_length=200, help_text='Обязателен для заполнения!')
    """
    Настройка формы для регистрации с изменениями в HTML форме.
    """
    class Meta:
        model = CustomUser
        fields = (
            "username", "email", "password1", "password2", "photo",
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
