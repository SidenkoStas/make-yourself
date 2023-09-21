from rest_framework.decorators import action
from rest_framework.response import Response
from likes.services import LikeServices
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class LikedMixin:
    """
    Mixin to add or delete like to obj.
    """
    @action(
        methods=["POST", "DELETE"],
        permission_classes=[IsAuthenticatedOrReadOnly],
        detail=True
    )
    def like(self, request, pk=None):
        """
        Manage obj's like
        """
        obj = self.get_object()
        like_services = LikeServices(obj, request.user)
        if request.method == "POST":
            like_services.add_like()
        elif request.method == "DELETE":
            like_services.remove_like()
        return Response()


class LikeSerializerMixin:
    """
    Parent class for managing like.
    """
    def to_representation(self, instance):
        """
        Counting total amount of likes to a post.
        """
        representation = super().to_representation(instance)
        representation['total_likes'] = instance.total_likes
        return representation

    def get_is_fan(self, obj) -> bool:
        """
        Check if user add like to a post or not.
        """
        user = self.context.get('request').user
        like_services = LikeServices(obj, user)
        return like_services.is_fan()
