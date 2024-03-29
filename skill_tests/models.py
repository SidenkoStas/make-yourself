from django.db import models
from django.contrib.auth import get_user_model
from random import shuffle


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
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Автор")
    question = models.TextField(verbose_name="Вопрос")

    def get_answers(self):
        answer_objs = list(Answer.objects.filter(question=self))
        data = []
        shuffle(answer_objs)

        for answer_obj in answer_objs:
            data.append({
                'answer': answer_obj.answer,
                'is_correct': answer_obj.is_correct
            })
        return data

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return f"{self.title}"


class Answer(models.Model):
    """
    Answer for questions model.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")
    is_correct = models.BooleanField(default=False, verbose_name="Корректность ответа")

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return f"{self.question[:10]} - {self.answer[:10]}"


class SkillTest(models.Model):
    """
    Test's model.
    """
    slug = models.SlugField(db_index=True, unique=True)
    title = models.CharField(max_length=150, verbose_name="Название теста")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Автор")
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
