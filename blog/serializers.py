from rest_framework import serializers
from blog.models import Category, Post, Comment
from likes.services import is_fan


class LikeBase:
    """
    Parent class for post and comment model to manage like.
    """
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['total_likes'] = instance.likes.count()
        return representation

    def get_is_fan(self, obj) -> bool:
        """
        Check liked user or not.
        """
        user = self.context.get('request').user
        return is_fan(obj, user)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PostSerializer(LikeBase, serializers.ModelSerializer):
    is_fan = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    is_fan = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"
