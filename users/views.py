from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import login, get_user_model
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.views import (PasswordResetConfirmView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetCompleteView)


class SignUpView(CreateView):
    """
    Представление для создания и управления регистрацией новых пользователей.
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
            form.save_m2m()

            # Берём нужную информацию, для отправки по email:
            token = default_token_generator.make_token(user)
            current_site = get_current_site(self.request)
            mail_subject = ("Ссылка активации направлена "
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
            try:
                email.send()
                message_text = """
                Пожалуйста, подтвердите свой 
                email для завершения регистрации!
                """
                return render(
                    self.request,
                    "users/information_message.html",
                    context={"message_text": message_text}
                )
            except:
                user.delete()
                message_text = "Что-то пошло не так, попробуйте ещё!"
                return render(
                    self.request,
                    "users/information_message.html",
                    context={"message_text": message_text}
                )


def activate(request, uid, token):
    """
    Представление для активации аккаунта зарегистрированного пользователя.
    Параметры передаются автоматически из письма активации.
    """
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
        # reverse_lazy не предоставляет response, поэтоме его нужно
        # предоставить вручную.
        return HttpResponseRedirect(reverse_lazy("common:index"))
    else:
        message_text = "Ссылка активации не действительна!"
        return render(
            request,
            "users/information_message.html",
            context={"message_text": message_text}
        )


class ProfileDetail(DetailView):
    """
    Представление для отображения страницы пользователя.
    """
    model = get_user_model()
    template_name = "users/profile_detail.html"


class UserUpdateView(UpdateView):
    """
    Представление для редактирования профиля пользователя.
    """
    model = get_user_model()
    template_name = "users/edit_profile.html"
    form_class = CustomUserChangeForm


class UserPasswordResetView(PasswordResetView):
    """
    Запрос информации для подтверждения сброса пароля.
    """
    email_template_name = "users/password_reset_mail.html"
    template_name = "users/password_reset.html"
    extra_email_context = {"context_message": "Ссылка для сброса пароля."}


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Отображение формы для сброса пароля.
    """
    template_name = 'users/password_reset.html'
    success_url = reverse_lazy("users:password_reset_complete")


class UserPasswordResetDoneView(PasswordResetDoneView):
    """
    Информация об отправке письма со сбросом пароля.
    """
    template_name = 'users/information_message.html'
    extra_context = {
        "message_text": "Ссылка для сброса пароля выслана по указанному email!"
    }


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    """
    При успешном изменении пароля.
    """
    template_name = 'users/information_message.html'
    extra_context = {
        "message_text":
            "Пароль успешно изменён. Войдитена сайт используя новый пароль."
    }
