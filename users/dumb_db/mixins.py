from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .services import ManageDbServices
from blog.models import Post
from rest_framework.response import Response
from rest_framework import status


class WorkWithDBMixin:
    """
    Mixin for work with db.
    Dumb and load db for user.
    """
    @action(
        methods=["GET", "POST"],
        permission_classes=(IsAuthenticated,),
        detail=True,

    )
    def save_db(self, request, id=None):
        """
        Dumb db for user
        """
        user_pk = request.user.pk
        if request.method == "GET":
            target_pk = Post.objects.filter(
                author=user_pk
            ).values_list("pk", flat=True),
            target_pk = ",".join(map(str, target_pk[0]))
            manage_db_services = ManageDbServices(user_pk, target_pk=target_pk)
            return manage_db_services.dump_db()

        elif request.method == "POST":
            file = request.FILES.get("file")
            if file is None:
                return Response({"error": "File not provided"},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                ManageDbServices(user_pk, file=file).load_db()
                return Response({"message": "Data loaded successfully"},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
