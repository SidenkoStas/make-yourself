from django.contrib.auth import get_user_model
from django.db import models


class Score(models.Model):
    """
    A model for evaluating an object from 1 to 5.
    """
    rating = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    score = models.SmallIntegerField(choices=rating, verbose_name="Оценка")
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    model_type = models.CharField(
        max_length=255, verbose_name="Связанная модель"
    )
    object_id = models.IntegerField(verbose_name="PK объекта")

    def __str__(self):
        return f"{self.user} - {self.score}"
