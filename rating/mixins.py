from rest_framework.decorators import action
from rest_framework.response import Response
from rating.services import RatingServices
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Avg


class RatingMixin:
    """
    Mixin to add or delete score to obj.
    """
    @action(
        methods=["POST", "DELETE"],
        permission_classes=[IsAuthenticatedOrReadOnly],
        detail=True
    )
    def score(self, request, pk=None):
        """
        Manage obj's rating.
        """
        obj = self.get_object()
        rating_services = RatingServices(obj, request.user)
        if request.method == "POST":
            try:
                score, is_created = rating_services.add_score(
                    score=request.data["score"]
                )
            except KeyError:
                return Response(
                    {"detail":
                         "Необходимо указать поле "
                         "'score' со значением от 1 до 5"}
                )
            if is_created:
                obj.rating.add(score)

        elif request.method == "DELETE":
            rating_services.remove_score()
        return Response({"detail": "Done"})

    # def get_queryset(self):
    #     """
    #     Add to common get_queryset average object's rating.
    #     """
    #     user = self.request.user
    #     queryset = super().get_queryset()
    #     queryset = queryset.annotate(average_rating=Avg("rating__score"))
    #     return queryset


class RatingSerializerMixin:
    """
    Parent class for managing rating.
    """
    def get_is_score(self, obj) -> int | bool:
        """
        Check if user add score to an object or not.
        """
        user = self.context.get("request").user
        rating_services = RatingServices(obj, user)
        return rating_services.get_rating()
