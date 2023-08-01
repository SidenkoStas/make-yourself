from django.db import models
from django.contrib.auth.models import AbstractUser


class Notification(models.Model):
    """
    Модель для управления уведомлений и новостей для пользователя.
    """
    slug = models.SlugField(max_length=250, unique=True, db_index=True)
    notification = models.CharField(max_length=150, verbose_name="Уведомление")

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def __str__(self):
        return f"{self.notification}"


class CustomUser(AbstractUser):
    """
    Доработанная модель пользователей с добавлением своих полей.
    """
    photo = models.ImageField(upload_to="profile_photo/%Y/%m/%d/", blank=True,
                              verbose_name="Фото профиля")
    bio = models.TextField(blank=True, verbose_name="О себе")
    notifications = models.ManyToManyField(
        Notification, blank=True, verbose_name="Уведомления"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.username}"
