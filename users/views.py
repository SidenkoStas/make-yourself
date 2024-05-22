from django.views.generic import DetailView
# from django.views.generic import UpdateView

from .models import CustomUser


class UserDetailView(DetailView):
    model = CustomUser
    template_name = "users/user_detail.html"

class UserEditView(DetailView):
    model = CustomUser
    template_name = "users/user_edit.html"