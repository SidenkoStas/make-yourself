from django.utils.text import slugify
from rest_framework.serializers import ValidationError


def set_slugify(request):
    """
    Set slugify for title.
    """
    try:
        request.data["slug"] = slugify(request.data["title"])
    except KeyError:
        raise ValidationError({"title": "Поле 'title' обязательно для заполнения"})
