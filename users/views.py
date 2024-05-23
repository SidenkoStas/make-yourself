from django.views.generic import DetailView
from django.views.generic import UpdateView

from .models import CustomUser


class UserDetailView(DetailView):
    """
    User detail view.
    """
    model = CustomUser
    template_name = "users/user_detail.html"


class UserEditView(UpdateView):
    """
    User edit view.
    """
    model = CustomUser
    template_name = "users/user_edit.html"
    fields = "__all__"
