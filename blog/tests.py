from django.test import TestCase
from blog.models import Post, Category, Comment
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, force_authenticate
from blog.views import PostsViewSet, CategoriesListView, CommentsViewSet

User = get_user_model()


class BaseTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(
            email="email@mail.ru",
            password="testing"
        )
        Token.objects.create(user=user)
        category = Category.objects.create(
            title="Test_Category",
            slug="test-category"
        )
        post = Post.objects.create(
            title="Test_Post",
            slug="test-post",
            content="Some content",
            author=user,
            category=category,
        )
        Comment.objects.create(
            author=user,
            post=post,
            content="Some comment"
        )


class CategoriesTest(BaseTest):
    """
    Test of Category model and it's API.
    """
    factory = APIRequestFactory()

    def test_get(self):
        view = CategoriesListView.as_view()
        request = self.factory.get("/blog/categories/", format="json")
        response = view(request)
        self.assertEqual(
            response.data,
            [{'id': 1, 'slug': 'test-category',
              'title': 'Test_Category'}]
        )


class PostTest(BaseTest):
    """
    Test of Post model and it's API.
    """
    factory = APIRequestFactory()

    def test_post(self):
        view = PostsViewSet.as_view({"post": "create"})
        user = User.objects.first()
        category = Category.objects.first()
        data = {"title": "Second_Post",
                "slug": "second-post",
                "content": "Some content again",
                "author": user.pk,
                "category": category.pk}
        request = self.factory.post("/blog/posts/", data=data, format="json")
        force_authenticate(request, user=user, token=user.auth_token)
        response = view(request)
        pk = response.data["id"]
        post_check = Post.objects.get(pk=pk)
        self.assertEqual(post_check.title, "Second_Post")
        self.assertEqual(post_check.slug, "second-post")
        self.assertEqual(post_check.content, "Some content again")

    def test_get(self):
        view = PostsViewSet.as_view({"get": "list"})
        request = self.factory.get("/blog/posts/", format="json")
        response = view(request)
        data = response.data["results"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["total_likes"],  0)
        self.assertEqual(data[0]["title"],  "Test_Post")
        self.assertEqual(data[0]["content"],  "Some content")

    def test_get_detail(self):
        view = PostsViewSet.as_view({"get": "retrieve"})
        post = Post.objects.first()
        request = self.factory.get(f"/blog/posts/", format="json")
        response = view(request, pk=post.pk)
        data = response.data
        self.assertEqual(data["title"], "Test_Post")
        self.assertEqual(data["slug"], "test-post")
        self.assertEqual(data["content"], "Some content")

    def test_patch_detail(self):
        user = User.objects.first()
        view = PostsViewSet.as_view({"patch": "update"})
        post = Post.objects.first()
        category = Category.objects.first()
        data = {"title": "Change_Post",
                "content": "Change content",
                "slug": "change-content",
                "author": user.pk,
                "category": category.pk}
        request = self.factory.patch(
            f"/blog/posts/", data=data, format="json"
        )
        force_authenticate(request, user=user, token=user.auth_token)
        response = view(request, pk=post.pk)
        data = response.data
        self.assertEqual(data["title"], "Change_Post")
        self.assertEqual(data["content"], "Change content")
        self.assertEqual(data["slug"], "change-content")

    def test_delete(self):
        view = PostsViewSet.as_view({"delete": "destroy"})
        user = User.objects.first()
        post = Post.objects.first()
        request = self.factory.delete(f"/blog/posts/", format="json")
        force_authenticate(request, user=user, token=user.auth_token)
        response = view(request, pk=post.pk)
        post = Post.objects.filter(pk=post.pk)
        self.assertEqual(post.exists(), False)


class CommentTest(BaseTest):
    """
    Test of Comment model and it's API.
    """
    factory = APIRequestFactory()

    def test_post(self):
        view = CommentsViewSet.as_view({"post": "create"})
        user = User.objects.first()
        post = Post.objects.first()
        data = {"author": user.pk,
                "content": "Some comment again",
                "post": post.pk}
        request = self.factory.post(
            "/blog/comments/", data=data, format="json"
        )
        force_authenticate(request, user=user, token=user.auth_token)
        response = view(request)
        pk = response.data["id"]
        comment_check = Comment.objects.get(pk=pk)
        self.assertEqual(comment_check.content, "Some comment again")

    def test_get(self):
        view = CommentsViewSet.as_view({"get": "list"})
        request = self.factory.get("/blog/comments/", format="json")
        response = view(request)
        data = response.data["results"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["total_likes"],  0)
        self.assertEqual(data[0]["content"],  "Some comment")

    def test_get_detail(self):
        view = CommentsViewSet.as_view({"get": "retrieve"})
        comment = Comment.objects.first()
        request = self.factory.get(f"/blog/posts/", format="json")
        response = view(request, pk=comment.pk)
        data = response.data
        self.assertEqual(data["content"], "Some comment")

    def test_patch_detail(self):
        user = User.objects.first()
        view = CommentsViewSet.as_view({"patch": "update"})
        post = Post.objects.first()
        comment = Comment.objects.first()
        data = {"content": "Change comment",
                "author": user.pk,
                "post": post.pk}
        request = self.factory.patch(
            f"/blog/comments/", data=data, format="json"
        )
        force_authenticate(request, user=user, token=user.auth_token)
        response = view(request, pk=comment.pk)
        data = response.data
        self.assertEqual(data["content"], "Change comment")

    def test_delete(self):
        view = CommentsViewSet.as_view({"delete": "destroy"})
        user = User.objects.first()
        comment = Comment.objects.first()
        request = self.factory.delete(f"/blog/comments/", format="json")
        force_authenticate(request, user=user, token=user.auth_token)
        response = view(request, pk=comment.pk)
        comment = Comment.objects.filter(pk=comment.pk)
        self.assertEqual(comment.exists(), False)
