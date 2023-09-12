from django.urls import path
from .forms import CustomAuthenticationForm
from .old_views import UserUpdateView, activate, SignUpView
from django.contrib.auth.views import LoginView, LogoutView
from .old_views import (UserPasswordResetView, UserPasswordResetConfirmView,
                        UserPasswordResetDoneView, UserPasswordResetCompleteView,
                        ProfileDetail)

app_name = "users"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(
        form_class=CustomAuthenticationForm,
        template_name="users/login.html"), name="login"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "profile_detail/<int:pk>/", ProfileDetail.as_view(),
        name="profile_detail"
    ),
    path(
        "edit_profile/<int:pk>/", UserUpdateView.as_view(), name="edit_profile"
    ),
    path(
        "password_reset/", UserPasswordResetView.as_view(),
        name="password_reset"
    ),
    path(
        "password_reset/done/", UserPasswordResetDoneView.as_view(),
        name="password_reset_done"
    ),
    path(
        'password_reset/confirm/<uidb64>/<token>/',
        UserPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        "password_reset/complete/", UserPasswordResetCompleteView.as_view(),
        name="password_reset_complete"
    ),
    path("activate/<str:uid>/<str:token>", activate, name="activate"),
]
