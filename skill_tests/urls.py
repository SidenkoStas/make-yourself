from django.urls import path
from .views import CreateTestView


urlpatterns = [
    path("tests/create_test/", CreateTestView.as_view(), name="create_test"),
]
