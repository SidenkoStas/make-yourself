from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Like(models.Model):
    """
    Likes model.
    """
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        verbose_name="Пользователь", null=True
    )
    content_type = models.ForeignKey(
        ContentType, null=True, on_delete=models.SET_NULL
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        "content_type", "object_id"
    )

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"
