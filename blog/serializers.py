from rest_framework import serializers
from blog.models import Category, Post, Comment
from likes.mixins import LikeSerializerMixin


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model
    """
    class Meta:
        model = Category
        fields = "__all__"


class PostSerializer(LikeSerializerMixin, serializers.ModelSerializer):
    """
    Serializer for Post model
    """
    is_fan = serializers.SerializerMethodField()
    published = serializers.BooleanField(source="is_published", default=False)
    view_counter = serializers.IntegerField(source="get_view_count")

    class Meta:
        model = Post
        fields = ["id", "slug", "published", "creation_date", "category",
                  "author", "title", "content", "publish_date", "is_fan",
                  "view_counter"]


class CommentSerializer(LikeSerializerMixin, serializers.ModelSerializer):
    """
    Serializer for Comment model
    """
    is_fan = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "creation_date", "author", "parent", "content", "post",
                  "is_fan", "children")
        extra_kwargs = {'children': {'required': False}}
