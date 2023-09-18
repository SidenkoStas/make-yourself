from django.urls import path, include
from blog.views import CategoriesListView, PostsViewSet, CommentsViewSet
from rest_framework.routers import DefaultRouter


app_name = "blog"

routers = DefaultRouter()
routers.register("posts", PostsViewSet, basename="posts")
routers.register("comments", CommentsViewSet, basename="comments")

urlpatterns = [
    path("categories/", CategoriesListView.as_view(), name="categories"),
    path("", include(routers.urls))
]
