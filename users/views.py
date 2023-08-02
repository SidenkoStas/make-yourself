from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate

from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy



class SignUpView(CreateView):
    """
    Представление для управления регистрацией новых пользователей.
    """
    model = get_user_model()
    template_name = "users/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("common:index")




