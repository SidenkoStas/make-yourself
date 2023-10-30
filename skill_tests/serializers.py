from rest_framework import serializers
from skill_tests.models import Category, Question, SkillTest


class CategorySerializer(serializers.ModelSerializer):
    """
    Category's serializer.
    """
    class Meta:
        model = Category
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    """
    Question's serializer.
    """
    class Meta:
        model = Question
        fields = "__all__"


class SkillTestSerializer(serializers.ModelSerializer):
    """
    Test of skill serializer.
    """
    class Meta:
        model = SkillTest
        fields = "__all__"
