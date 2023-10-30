from django.db import models


class Category(models.Model):
    """
    Test's category model.
    """
    slug = models.SlugField(db_index=True, unique=True)
    title = models.CharField(max_length=150, verbose_name="Категория")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.title}"


class Question(models.Model):
    """
    Question for tests model.
    """
    slug = models.SlugField(db_index=True)
    title = models.CharField(max_length=255)
    question = models.TextField(verbose_name="Вопрос")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return f"{self.title}"


class SkillTest(models.Model):
    """
    Test's model.
    """
    slug = models.SlugField(db_index=True, unique=True)
    title = models.CharField(max_length=150, verbose_name="Название теста")
    description = models.TextField(verbose_name="Описание теста")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name="Категория"
    )
    questions = models.ManyToManyField(
        Question, verbose_name="Вопросы", blank=True
    )
    creation_time = models.DateTimeField(
        auto_now=True, verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def __str__(self):
        return f"{self.slug}"


class TestStatistic(models.Model):
    """
    Test's statistic model.
    """
    pass
