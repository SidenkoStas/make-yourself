from rest_framework.mixins import CreateModelMixin
from rest_framework import serializers
from django.utils.text import slugify


class CustomCreateModelMixin(CreateModelMixin):
    """
    Add custom create method with slugify.
    """
    def create(self, request, *args, **kwargs):
        request.data["author"] = request.user.pk
        try:
            request.data["slug"] = slugify(request.data["title"])
        except KeyError:
            raise serializers.ValidationError({"title": "Поле 'title' обязательно для заполнения"})
        return super().create(request, *args, **kwargs)
