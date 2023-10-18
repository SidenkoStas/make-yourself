from rest_framework import serializers
from blog.models import Category, Post, Comment
from likes.mixins import LikeSerializerMixin
from rating.mixins import RatingSerializerMixin


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model
    """
    class Meta:
        model = Category
        fields = "__all__"


class ListPostsSerializer(LikeSerializerMixin,
                          RatingSerializerMixin,
                          serializers.ModelSerializer):
    """
    Serializer for list of posts
    """
    total_likes = serializers.IntegerField(read_only=True)
    amount_comments = serializers.IntegerField(read_only=True)
    view_count = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Post
        fields = ["title", "category", "creation_date", "author", "content",
                  "view_count", "total_likes", "amount_comments",
                  "average_rating"]


class PostSerializer(ListPostsSerializer):
    """
    Serializer for Post model
    """
    is_fan = serializers.SerializerMethodField()
    published = serializers.BooleanField(source="is_published", default=False)
    is_score = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "slug", "published", "creation_date", "category",
                  "author", "title", "content", "publish_date", "is_fan",
                  "view_count", "total_likes", "amount_comments", "is_score",
                  "average_rating"]


class CommentSerializer(LikeSerializerMixin, serializers.ModelSerializer):
    """
    Serializer for Comment model
    """
    is_fan = serializers.SerializerMethodField()
    total_likes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "creation_date", "author", "parent", "content", "post",
                  "is_fan", "children", "total_likes")
        extra_kwargs = {'children': {'required': False}}
