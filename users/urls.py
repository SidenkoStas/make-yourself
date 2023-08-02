from django.urls import path
from .views import SignUpView
from django.contrib.auth.views import LoginView, LogoutView


app_name = "users"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(
        template_name="users/login.html"), name="login"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("edit_profile/", SignUpView.as_view(), name="edit_profile"),
]
