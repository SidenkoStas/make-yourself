from rest_framework.decorators import action
from rest_framework.response import Response
from likes import services
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from likes.services import is_fan


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
        print(request)
        obj = self.get_object()
        if request.method == "POST":
            services.add_like(obj, request.user)
        elif request.method == "DELETE":
            services.remove_like(obj, request.user)
        return Response()


class LikeSerializerMixin:
    """
    Parent class for post and comment model to manage like.
    """
    def to_representation(self, instance):
        """
        Counting total amount of likes to a post.
        """
        representation = super().to_representation(instance)
        representation['total_likes'] = instance.likes.count()
        return representation

    def get_is_fan(self, obj) -> bool:
        """
        Check if user add like to post  or not.
        """
        user = self.context.get('request').user
        return is_fan(obj, user)
