from django.db import models


class Category(models.Model):
    slug = models.SlugField(db_index=True, unique=True)
    name = models.CharField(max_length=150, verbose_name="Категория")

    def __str__(self):
        return f"{self.name}"


class SkillTest(models.Model):
    slug = models.SlugField(db_index=True, unique=True)
    name = models.CharField(max_length=150, verbose_name="Название теста")
    description = models.TextField(verbose_name="Описание теста")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name="Категория"
    )

    def __str__(self):
        return f"{self.slug}"


class Question(models.Model):
    question = models.TextField(verbose_name="Вопрос")

    test = models.ManyToManyField(SkillTest, verbose_name="Тест")


class TestStatistic(models.Model):
    pass
