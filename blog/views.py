from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from blog.models import Category, Post, Comment
from blog.serializers import (CategorySerializer, PostSerializer,
                              CommentSerializer)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from likes.mixins import LikedMixin


class CategoriesListView(ListAPIView):
    """
    View for list all category of blog
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostsViewSet(LikedMixin, ModelViewSet):
    """
    View for manage posts of blog
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class CommentsViewSet(LikedMixin, ModelViewSet):
    """
    View for manage comments of blog's posts
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
