from django.urls import path
from .views import UserUpdateView, activate, SignUpView
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordResetDoneView,
                                       PasswordResetCompleteView)
from .views import UserPasswordResetView, UserPasswordResetConfirmView

app_name = "users"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(
        template_name="users/login.html"), name="login"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "edit_profile/<int:pk>/", UserUpdateView.as_view(), name="edit_profile"
    ),
    path(
        "password_reset/", UserPasswordResetView.as_view(),
        name="password_reset"
    ),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name="password_reset_done"
    ),
    path(
        'password_reset/confirm/<uidb64>/<token>/',
        UserPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        "password_reset/complete/",
        PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ), name="password_reset_complete"
    ),
    path("activate/<str:uid>/<str:token>", activate, name="activate"),
]
