from django.urls import path
from .views import UserDetailView, UserEditView


app_name = "users"

urlpatterns = [
    path("<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("edit/<int:pk>/", UserEditView.as_view(), name="user_edit"),
]
