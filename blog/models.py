from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from likes.models import Like
from mptt.models import TreeForeignKey, MPTTModel
from rating.models import Score


class PostCommentBase(models.Model):
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


class View(models.Model):
    """
    View model.
    """
    article = models.ForeignKey("Post", on_delete=models.CASCADE,
                                related_name="views")
    ipaddress = models.GenericIPAddressField(verbose_name="IP адресс")

    class Meta:
        verbose_name = "Просмотр"
        verbose_name_plural = "Просмотры"

    def __str__(self):
        return f"{self.article} - {self.ipaddress}"


class Category(models.Model):
    """
    Blog's category model.
    """
    slug = models.SlugField(db_index=True, unique=True)
    title = models.CharField(max_length=255, verbose_name="Категория")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.title}"


class Post(PostCommentBase):
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
    rating = models.ManyToManyField(
        Score, blank=True, related_name="post",
        verbose_name="Оценка"
    )

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return f"{self.title}"


class Comment(MPTTModel, PostCommentBase):
    """
    Comment for the Post model.
    """
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    parent = TreeForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE,
        verbose_name="Родительский комментарий",
        related_name='children'
    )

    class MTTMeta:
        order_insertion_by = ('-creation_date',)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-creation_date"]

    def __str__(self):
        return f"Author: {self.author_id} | Post: {self.post_id}"
