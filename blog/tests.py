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
    def test_get(self):
        self.assertEqual(
            self.client.get("/blog/categories/").data,
            [{'id': 1, 'slug': 'test-category',
              'title': 'Test_Category'}]
        )


class PostTest(BaseTest):
    """
    Test of Post model and it's API.
    """

    def test_post(self):
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

        pk = post.data["id"]
        post_check = Post.objects.get(pk=pk)
        self.assertEqual(post_check.title, "Second_Post")
        self.assertEqual(post_check.slug, "second-post")
        self.assertEqual(post_check.content, "Some content again")

    def test_get(self):
        get = self.client.get("/blog/posts/")
        self.assertEqual(len(get.json()), 1)
        self.assertEqual(get.json()[0]["total_likes"],  0)
        self.assertEqual(get.json()[0]["title"],  "Test_Post")
        self.assertEqual(get.json()[0]["slug"],  "test-post")

    def test_get_detail(self):
        user = User.objects.first()
        self.client.force_login(user)
        post = Post.objects.first()
        self.client.get(f"/blog/posts/{post.pk}/")
        self.assertEqual(post.title, "Test_Post")
        self.assertEqual(post.slug, "test-post")
        self.assertEqual(post.content, "Some content")

    def test_patch_detail(self):
        user = User.objects.first()
        self.client.force_login(user)
        post = Post.objects.first()
        self.client.patch(
            f"/blog/posts/{post.pk}/",
            {"title": "Change_Post",
             "content": "Change content"},
            content_type='application/json',
        )
        post = Post.objects.first()
        self.assertEqual(post.title, "Change_Post")
        self.assertEqual(post.content, "Change content")

    def test_delete(self):
        user = User.objects.first()
        self.client.force_login(user)
        post = Post.objects.first()
        pk = post.pk
        self.client.delete(f"/blog/posts/{pk}/")
        post = Post.objects.filter(pk=pk)
        self.assertEqual(bool(post), False)


class CommentTest(BaseTest):
    """
    Test of Comment model and it's API.
    """
    def test_post(self):
        user = User.objects.first()
        post = Category.objects.first()
        self.client.force_login(user)
        comment = self.client.post(
            "/blog/comments/",
            {"author": user.pk,
             "content": "Some comment again",
             "post": post.pk}
        )

        pk = comment.data["id"]
        comment_check = Comment.objects.get(pk=pk)
        self.assertEqual(comment_check.content, "Some comment again")

    def test_get(self):
        get = self.client.get("/blog/comments/")
        self.assertEqual(len(get.json()), 1)
        self.assertEqual(get.json()[0]["total_likes"],  0)
        self.assertEqual(get.json()[0]["content"],  "Some comment")

    def test_get_detail(self):
        user = User.objects.first()
        self.client.force_login(user)
        comment = Comment.objects.first()
        self.client.get(f"/blog/comments/{comment.pk}/")
        self.assertEqual(comment.content, "Some comment")

    def test_patch_detail(self):
        user = User.objects.first()
        self.client.force_login(user)
        comment = Comment.objects.first()
        self.client.patch(
            f"/blog/comments/{comment.pk}/",
            {"content": "Change comment"},
            content_type='application/json',
        )
        comment = Comment.objects.first()
        self.assertEqual(comment.content, "Change comment")

    def test_delete(self):
        user = User.objects.first()
        self.client.force_login(user)
        comment = Comment.objects.first()
        pk = comment.pk
        self.client.delete(f"/blog/comments/{pk}/")
        comment = Comment.objects.filter(pk=pk)
        self.assertEqual(bool(comment), False)
