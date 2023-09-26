from django.forms import model_to_dict
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response


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
