from django.urls import path, include
from users.api_views import activate_profile, password_reset, CustomUserViewSet
from rest_framework.routers import DefaultRouter


app_name = "users"
router = DefaultRouter()
router.register("users", CustomUserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls.authtoken")),
    path("activate/<str:uid>/<str:token>/",
         activate_profile, name="activate_profile"),
    path("password/reset/confirm/<str:uid>/<str:token>/",
         password_reset, name="password_reset_confirm")
]
