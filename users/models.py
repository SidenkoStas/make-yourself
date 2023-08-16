import time

from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser


def user_directory_path(instance, filename):
    """
    Функция сохранения загруженных файлов в дерикторию, с учётом мользователя
    и названия файла.
    """
    prefix = time.strftime("%Y/%m/%d")
    return f'profile_photo/{prefix}/user_{instance.username}/{filename}'


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
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to=user_directory_path, blank=True,
                              verbose_name="Фото профиля")
    bio = models.TextField(blank=True, verbose_name="О себе")
    notifications = models.ManyToManyField(
        Notification, blank=True, verbose_name="Уведомления"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def get_notifications(self):
        """
        Возвращает список уведомлений к которым подписан пользователь.
        """
        return ", ".join(
            [p.notification for p in self.notifications.all()])

    def get_absolute_url(self):
        return reverse("users:edit_profile", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.username}"
