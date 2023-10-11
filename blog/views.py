from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from blog.mixins import CustomCreateModelMixin
from blog.models import Category, Post, Comment
from blog.serializers import (CategorySerializer, PostSerializer,
                              CommentSerializer, ListPostsSerializer)
from make_yourself.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from likes.mixins import LikedMixin
from blog.mixins import ViewMixin


class CategoriesListView(ListAPIView):
    """
    View for list all category of blog
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostsViewSet(LikedMixin,
                   ViewMixin,
                   CustomCreateModelMixin,
                   ModelViewSet):
    """
    View for manage posts of blog
    """
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )

    def get_serializer_class(self):
        if self.action == 'list':
            return ListPostsSerializer
        return PostSerializer

    def get_queryset(self):
        """
        Add to common get_queryset prefetch view to a post.
        """
        queryset = super().get_queryset()
        queryset = (
            queryset.prefetch_related("views").order_by("-creation_date")
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
        queryset = queryset.prefetch_related('children')
        return queryset
