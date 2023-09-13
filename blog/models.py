from django.db import models
from django.contrib.auth import get_user_model


class PostBase(models.Model):
    """
    Абстрактная модель для постов и комментов.
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


class Category(models.Model):
    """
    Модель категорий для постов блога.
    """
    slug = models.SlugField(db_index=True)
    title = models.CharField(max_length=255, verbose_name="Категория")

    def __str__(self):
        return f"{self.title}"


class Post(PostBase):
    """
    Модель постов блога.
    """
    PUB = (
        (0, "Не опубликован"),
        (1, "Опубликован")
    )

    slug = models.SlugField(db_index=True)
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    is_published = models.BooleanField(
        default=0, choices=PUB, verbose_name="Опубликован"
    )
    publish_date = models.DateTimeField(
        null=True, default=None, verbose_name="Дата публикации"
    )

    def __str__(self):
        return f"{self.title}"


class Comment(PostBase):
    """
    Модель комментариев к посту.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author}"
