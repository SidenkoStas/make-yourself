from django.test import TestCase
from blog.models import Post, Category, Comment
from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()


class BaseTest(TestCase):
    def setUp(self) -> None:
        client = Client()
        user = User.objects.create(
            email="email@mail.ru",
            password="testing"
        )
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
    def test_create_category(self):
        category = Category.objects.first()
        self.assertEqual(
            self.client.get("/blog/categories/").data,
            [{'id': 1, 'slug': 'test-category', 'title': 'Test_Category'}]
        )


class ModelTest(BaseTest):
    """
    Test of Post model and it's API.
    """
    def test_create_post(self):
        user = User.objects.first()
        category = Category.objects.first()
        self.client.force_login(user)
        post = self.client.post(
            "/blog/posts/",
            {"title": "Second_Post",
             "slug": "second-post",
             "content": "Some content again",
             "author": user.pk,
             "category": category.pk}
        )

        id = post.data["id"]
        self.assertEqual(
            post.data,
            self.client.get(f"/blog/posts/{id}/").data
        )


class CommentTest(BaseTest):
    """
    Test of Comment model and it's API.
    """
    def test_create_comment(self):
        comment = Comment.objects.first()
        self.assertEqual(comment.content, "Some comment")
