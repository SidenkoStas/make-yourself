from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import authenticate, login, get_user_model
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site


class SignUpView(CreateView):
    """
    Представление для управления регистрацией новых пользователей.
    """
    model = get_user_model()
    template_name = "users/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("common:index")


    def form_valid(self, form):
        """
        Функция автоматической авторизации пользователя после регистрации.
        Сохраняет информацию в поля многие ко многим.
        """
        valid = super(SignUpView, self).form_valid(form)
        # form.save_m2m()
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # Берём нужную информацию, для отправки по email:
        token = default_token_generator.make_token(user)
        current_site = get_current_site(self.request)
        mail_subject = "Ссылка активации направлена Вам на указанный e-mail."
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


class UserUpdateView(UpdateView):
    model = get_user_model()
    fields = [
        "username", "photo", "email", "first_name", "last_name", "bio",
        "notifications"
    ]
    template_name = "users/edit_profile.html"
