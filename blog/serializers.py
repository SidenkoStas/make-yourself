from rest_framework import serializers
from blog.models import Category, Post, Comment


class PostSerializer(serializers.Serializer):
    class Meta:
        model = Post
        fields = "__all__"
