from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import login, get_user_model
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import (PasswordResetConfirmView,
                                       PasswordResetView)



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
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # Берём нужную информацию, для отправки по email:
            token = default_token_generator.make_token(user)
            current_site = get_current_site(self.request)
            mail_subject = ("Ссылка активации направлена"
                            "Вам на указанный e-mail.")
            context_message = "Пожалуйста, перейди по ссылку для подтверждения регистрации!"
            message = render_to_string(
                "users/activate_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": token,
                    "context_message": context_message
                }
            )
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse(
                """
                Пожалуйста, подтвердите свой
                email для завершения регистрации!
                """
            )


def activate(request, uid, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse_lazy("common:index"))
    else:
        return HttpResponse("Ссылка активации не действительна!")


class UserUpdateView(UpdateView):
    model = get_user_model()
    fields = [
        "username", "photo", "email", "first_name", "last_name", "bio",
        "notifications"
    ]
    template_name = "users/edit_profile.html"


class UserPasswordResetView(PasswordResetView):
    email_template_name = "users/password_reset_mail.html"
    template_name = "users/password_reset.html"
    extra_email_context = {"context_message": "Ссылка для сброса пароля."}


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset.html'
    success_url = reverse_lazy("users:password_reset_complete")
