from rest_framework.generics import ListAPIView
from skill_tests.models import Category, Question, SkillTest
from skill_tests.serializers import (CategorySerializer, QuestionSerializer,
                                     SkillTestSerializer)
from rest_framework.viewsets import ModelViewSet
from make_yourself.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CategoriesView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = (
            queryset.order_by("title"))
        return queryset


class SkillTestViewSet(ModelViewSet):
    queryset = SkillTest.objects.all()
    serializer_class = SkillTestSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = (
            queryset.prefetch_related("questions").order_by("-creation_time"))
        return queryset
