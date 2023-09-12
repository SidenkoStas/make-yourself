from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    """
    Модель категорий для постов блога.
    """
    slug = models.SlugField()
    title = models.CharField(max_length=255, verbose_name="Категория")

    def __str__(self):
        return f"{self.title}"


class Post(models.Model):
    """
    Модель постов блога.
    """
    slug = models.SlugField()
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    posted_time = models.DateTimeField(
        blank=True, verbose_name="Дата публикации"
    )
    is_published = models.BooleanField(
        default=False, verbose_name="Опубликован"
    )
    author = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, verbose_name="Автор"
    )
    content = models.TextField(verbose_name="Контент")

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE,
        verbose_name="Автор комментария"
    )
    context = models.TextField(verbose_name="Комментарий")
