from rest_framework import serializers
from skill_tests.models import Category, Question, SkillTest, Answer


class CategorySerializer(serializers.ModelSerializer):
    """
    Category's serializer.
    """
    class Meta:
        model = Category
        fields = ("id", "title")


class QuestionSerializer(serializers.ModelSerializer):
    """
    Question's serializer.
    """
    answers = serializers.ListField(source="get_answers", read_only=True)

    class Meta:
        model = Question
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    """
    Answer's serializer.
    """
    class Meta:
        model = Answer
        fields = "__all__"


class SkillTestSerializer(serializers.ModelSerializer):
    """
    Serializer of test of skill .
    """

    class Meta:
        model = SkillTest
        fields = "__all__"
