from django.urls import path, include
from users.views import activate_profile, password_reset


app_name = "users"


urlpatterns = [
    path("", include("djoser.urls")),
    path("", include("djoser.urls.authtoken")),
    path("activate/<str:uid>/<str:token>/",
         activate_profile, name="activate_profile"),
    path("password/reset/confirm/<str:uid>/<str:token>/",
         password_reset, name="password_reset_confirm")
]
