from django.forms import model_to_dict
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from blog.services import get_client_ip
from blog.models import View, Post


class CustomCreateModelMixin(CreateModelMixin):
    """
    Fix response for POST request.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = model_to_dict(super().get_queryset().last())
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class ViewMixin:
    """
    Mixin for increase number of views.
    """
    def get_object(self):
        """
        Get object. Check and add unique view for user.
        """
        obj = super().get_object()
        ip_address = get_client_ip(self.request)
        View.objects.get_or_create(article=obj, ipaddress=ip_address)
        return obj
