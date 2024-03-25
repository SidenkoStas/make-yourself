from django.db.models import Count, Q
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from blog.services import get_client_ip
from blog.models import View
from make_yourself.services import set_slugify


class CustomCreateModelMixin(CreateModelMixin):
    """
    Fix response for POST request.
    """
    def create(self, request, *args, **kwargs):
        request.data["author"] = request.user.pk
        set_slugify(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        try:
            slug = request.data["slug"]
            data = model_to_dict(super().get_queryset().get(slug=slug))
        except KeyError:
            content = request.data["content"]
            data = model_to_dict(super().get_queryset().get(content=content))
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class ViewMixin:
    """
    Mixin for increase number of views.
    """
    def get_object(self):
        """
        Get object. Check and add unique view for a user.
        """
        obj = super().get_object()
        ip_address = get_client_ip(self.request)
        View.objects.get_or_create(article=obj, ipaddress=ip_address)
        return obj

    def get_queryset(self):
        """
        Add to common get_queryset with counting views to a post.
        """
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            view_count=Count("views", distinct=True))
        return queryset


class CountComments:
    """
    Mixin for counting amount of comments.
    """
    def get_queryset(self):
        """
        Add to common get_queryset with counting comments to a post.
        """
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            amount_comments=Count(
                "comments", distinct=True, filter=Q(comments__level=0)
            )
        )
        return queryset
