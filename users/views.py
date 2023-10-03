from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
import requests


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
        print(request.headers["Authorization"])
        if req.status_code == 400:
            return Response({"message": "Bad request!"})
        logout_url = "http://127.0.0.1:8000/account/token/logout/"
        headers = {"Authorization": request.headers["Authorization"]}
        requests.post(logout_url, headers=headers)
        return Response({"message": "Пароль успешно изменён!"})
    else:
        return Response({"message": "Введите и подтвердите новый пароль."
                                    "(new_password, re_new_password)"})
