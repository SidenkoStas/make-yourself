from .models import CustomUser, Notification
from django.contrib.auth.forms import (UserChangeForm, UserCreationForm,
                                       AuthenticationForm)
from django import forms


class CustomUserCreationForm(UserCreationForm):
    """
    Настройка формы для регистрации с изменениями в HTML форме.
    """
    class Meta:
        model = CustomUser
        fields = (
            "username", "email", "password1", "password2", "notifications"
        )
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    notifications = forms.ModelMultipleChoiceField(
        queryset=Notification.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={"checked": ""},
        ),
    )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={"class": "form-control", 'placeholder': 'Пароль'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={"class": "form-control", 'placeholder': 'Подтвердите пароль'})


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
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "photo": forms.FileInput(attrs={"class": "form-control col"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
        }

    notifications = forms.ModelMultipleChoiceField(
        queryset=Notification.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            {"class": "col", }
        ),
    )


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
