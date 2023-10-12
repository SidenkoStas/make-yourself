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


class ListPostsSerializer(LikeSerializerMixin,
                          serializers.ModelSerializer):
    """
    Serializer for list of posts
    """
    total_likes = serializers.IntegerField()
    amount_comments = serializers.IntegerField()
    view_count = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ["title", "category", "creation_date", "author", "content",
                  "view_count", "total_likes", "amount_comments"]


class PostSerializer(ListPostsSerializer):
    """
    Serializer for Post model
    """
    is_fan = serializers.SerializerMethodField()
    published = serializers.BooleanField(source="is_published", default=False)

    class Meta:
        model = Post
        fields = ["id", "slug", "published", "creation_date", "category",
                  "author", "title", "content", "publish_date", "is_fan",
                  "view_count", "total_likes", "amount_comments"]


class CommentSerializer(LikeSerializerMixin, serializers.ModelSerializer):
    """
    Serializer for Comment model
    """
    is_fan = serializers.SerializerMethodField()
    total_likes = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ("id", "creation_date", "author", "parent", "content", "post",
                  "is_fan", "children", "total_likes")
        extra_kwargs = {'children': {'required': False}}
