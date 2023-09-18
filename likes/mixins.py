from rest_framework.decorators import action
from rest_framework.response import Response
from likes import services
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
        print(request)
        obj = self.get_object()
        if request.method == "POST":
            services.add_like(obj, request.user)
        elif request.method == "DELETE":
            services.remove_like(obj, request.user)
        return Response()
