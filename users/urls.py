from rest_framework.routers import DefaultRouter
from django.urls import path, include
# from users.views import UserViewSet
from rest_framework.authtoken import views


app_name = "users"

# router = DefaultRouter()
# router.register("user", UserViewSet, basename="user")


urlpatterns = [
    path("", include("djoser.urls")),
    # path('token/', views.obtain_auth_token)
    path("", include('djoser.urls.authtoken')),
]
