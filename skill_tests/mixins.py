from rest_framework.mixins import CreateModelMixin
from rest_framework import serializers
from django.utils.text import slugify
from make_yourself.services import set_slugify


class CustomCreateModelMixin(CreateModelMixin):
    """
    Add custom create method with slugify.
    """
    def create(self, request, *args, **kwargs):
        request.data["author"] = request.user.pk
        set_slugify(request)
        return super().create(request, *args, **kwargs)
