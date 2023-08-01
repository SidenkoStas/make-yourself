from django.urls import include, path
from .views import UserViewSet, SignUpView
from rest_framework.routers import SimpleRouter


app_name = "users"


router = SimpleRouter()
router.register("account", UserViewSet, basename="user")
print(router.urls)

urlpatterns = [
    path("", include(router.urls)),
    path("signup/", SignUpView.as_view()),
]
