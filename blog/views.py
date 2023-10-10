from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from blog.mixins import CustomCreateModelMixin
from blog.models import Category, Post, Comment
from blog.serializers import (CategorySerializer, PostSerializer,
                              CommentSerializer)
from make_yourself.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from likes.mixins import LikedMixin


class CategoriesListView(ListAPIView):
    """
    View for list all category of blog
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostsViewSet(LikedMixin,
                   CustomCreateModelMixin,
                   ModelViewSet):
    """
    View for manage posts of blog
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )


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
