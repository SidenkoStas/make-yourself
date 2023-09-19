from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from likes.models import Like


class PostBase(models.Model):
    """
    Abstract model for Comment and Post models.
    """
    class Meta:
        abstract = True

    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    content = models.TextField(verbose_name="Содержание")
    creation_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    likes = GenericRelation(Like)


class Category(models.Model):
    """
    Category for blog's posts
    """
    slug = models.SlugField(db_index=True, unique=True)
    title = models.CharField(max_length=255, verbose_name="Категория")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.title}"


class Post(PostBase):
    """
    Blog's post model
    """
    PUB = (
        (0, "Не опубликован"),
        (1, "Опубликован")
    )

    slug = models.SlugField(db_index=True, unique=True)
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name="Категория"
    )
    is_published = models.BooleanField(
        default=0, choices=PUB, verbose_name="Публикация"
    )
    publish_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата публикации"
    )

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return f"{self.title}"


class Comment(PostBase):
    """
    Comment for Post model
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"{self.author}"
