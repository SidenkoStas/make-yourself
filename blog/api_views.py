from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from blog.mixins import CustomCreateModelMixin, CountComments
from blog.models import Category, Post, Comment
from blog.serializers import (CategorySerializer, PostSerializer,
                              CommentSerializer, ListPostsSerializer)
from make_yourself.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from likes.mixins import LikedMixin
from blog.mixins import ViewMixin
from rating.mixins import RatingMixin
from blog.filters import ProductFilter
from rest_framework.renderers import TemplateHTMLRenderer


class CategoriesListView(ListAPIView):
    """
    View for list all category of blog
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class PostsViewSet(LikedMixin,
                   RatingMixin,
                   ViewMixin,
                   CountComments,
                   CustomCreateModelMixin,
                   ModelViewSet):
    """
    View for manage posts of blog
    """
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )
    filterset_class = ProductFilter
    filter_backends = (DjangoFilterBackend, )
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "users/test.html"

    def get_serializer_class(self):
        """
        Return suitable serializer based on an action.
        """
        if self.action == "list":
            return ListPostsSerializer
        return PostSerializer

    def get_queryset(self):
        """
        Add to common get_queryset prefetch view to a post.
        """
        queryset = super().get_queryset()

        queryset = (
            queryset.order_by("-creation_date")
        )
        return queryset


class CommentsViewSet(LikedMixin,
                      CustomCreateModelMixin,
                      ModelViewSet):
    """
    View for manage comments of blog's posts
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )

    def get_queryset(self):
        """
        Add to common get_queryset prefetch comment children.
        """
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("children")
        return queryset
