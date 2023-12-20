from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from os import path, remove
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from blog.mixins import CustomCreateModelMixin, CountComments
from blog.models import Category, Post, Comment
from blog.serializers import (CategorySerializer, PostSerializer,
                              CommentSerializer, ListPostsSerializer)
from make_yourself.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from likes.mixins import LikedMixin
from blog.mixins import ViewMixin
from rating.mixins import RatingMixin
from blog.filters import ProductFilter
from django.http import FileResponse
from django.core.management import call_command


class CategoriesListView(ListAPIView):
    """
    View for list all category of blog
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class PostsViewSet(LikedMixin,
                   RatingMixin,
                   ViewMixin,
                   CountComments,
                   CustomCreateModelMixin,
                   ModelViewSet):
    """
    View for manage posts of blog
    """
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )
    filterset_class = ProductFilter
    filter_backends = (DjangoFilterBackend, )

    def get_serializer_class(self):
        """
        Return suitable serializer based on an action.
        """
        if self.action == "list":
            return ListPostsSerializer
        return PostSerializer

    def get_queryset(self):
        """
        Add to common get_queryset prefetch view to a post.
        """
        queryset = super().get_queryset()

        queryset = (
            queryset.order_by("-creation_date")
        )
        return queryset


class CommentsViewSet(LikedMixin,
                      CustomCreateModelMixin,
                      ModelViewSet):
    """
    View for manage comments of blog's posts
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )

    def get_queryset(self):
        """
        Add to common get_queryset prefetch comment children.
        """
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("children")
        return queryset


class WorkWithDBView(APIView):
    """
    View for work with db.
    Dumb and load db for user.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        posts_pk = Post.objects.filter(
            author=request.user.pk
        ).values_list("pk", flat=True),
        posts_pk = ",".join(map(str, posts_pk[0]))
        file_name = f"{request.user.pk}_db.json"
        file_path = path.join(
            settings.MEDIA_ROOT, file_name
        )
        # Сохраняем данные из базы данных с помощью команды dumpdata
        with open(file_path, "w") as db_dump:
            call_command("dumpdata", "blog.Post", pks=posts_pk,
                         stdout=db_dump)

        response = FileResponse(open(file_path, "rb"))
        response['Content-Disposition'] = f"attachment; filename='{file_name}'"
        remove(file_path)
        return response

    def post(self, request):
        file = request.FILES.get("file")
        if file is None:
            return Response({"error": "File not provided"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            file_path = path.join(settings.MEDIA_ROOT, file.name)
            print(file.name)
            # Сохраняем файл на сервере
            with open(file_path, "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Загружаем данные из файла с помощью команды loaddata
            call_command("loaddata", file_path)

            remove(file_path)
            return Response({"message": "Data loaded successfully"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
