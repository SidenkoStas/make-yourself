from rest_framework import serializers
from blog.models import Category, Post, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_total_likes(self, obj):
        return obj.likes.count()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
