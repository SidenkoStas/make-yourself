from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
import requests
from djoser.views import UserViewSet
from django.utils.timezone import now
from djoser import signals
from djoser.conf import settings
from rest_framework import status
from users.tasks import send_email
from users.services import get_email_context
from .dumb_db.mixins import WorkWithDBMixin


class CustomUserViewSet(WorkWithDBMixin, UserViewSet):
    """
    Manage users.
    """
    @action(["post"], detail=False)
    def activation(self, request, *args, **kwargs):
        """
        Account activation through email link.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        user.save()

        signals.user_activated.send(
            sender=self.__class__, user=user, request=self.request
        )

        if settings.SEND_CONFIRMATION_EMAIL:
            send_email.delay(
                *get_email_context(user, request),
                "confirmation"
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False)
    def resend_activation(self, request, *args, **kwargs):
        """
        Resend activation email.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user(is_active=False)

        if user:
            send_email.delay(
                *get_email_context(user, request),
                "activation"
            )
        return Response(status=status.HTTP_200_OK)

    @action(["post"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()

        if user:
            send_email.delay(
                *get_email_context(user, request),
                "password_reset"
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False)
    def reset_password_confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.user.set_password(serializer.data["new_password"])
        if hasattr(serializer.user, "last_login"):
            serializer.user.last_login = now()
        serializer.user.save()

        if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
            send_email.delay(
                *get_email_context(serializer.user, request),
                "password_changed_confirmation"
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def activate_profile(request, uid, token):
    """
    Account activation through email link.
    """
    url = "http://127.0.0.1:8000/account/users/activation/"
    data = {"uid": uid, "token": token}
    requests.post(url, data=data)
    return Response({"message": "Аккаунт активирован. Теперь вы можете войти"
                                " на сайт используя свою почту!"})


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def password_reset(request, uid, token):
    """
    Get new password and change it with logout.
    """
    if request.method == "POST":
        url = "http://127.0.0.1:8000/account/users/reset_password_confirm/"
        data = {"uid": uid, "token": token,
                "new_password": request.data["new_password"],
                "re_new_password": request.data["re_new_password"]
                }
        req = requests.post(url, data=data)
        if req.status_code == 400:
            return Response({"message": "Bad request!"})
        logout_url = "http://127.0.0.1:8000/account/token/logout/"
        headers = {"Authorization": request.headers["Authorization"]}
        requests.post(logout_url, headers=headers)
        return Response({"message": "Пароль успешно изменён!"})
    else:
        return Response({"message": "Введите и подтвердите новый пароль."
                                    "(new_password, re_new_password)"})
