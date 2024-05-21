from rest_framework.generics import ListAPIView
from skill_tests.models import Category, Question, Answer, SkillTest
from skill_tests.serializers import (CategorySerializer, QuestionSerializer,
                                     AnswerSerializer, SkillTestSerializer)
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from make_yourself.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import mixins
from skill_tests.mixins import CustomCreateModelMixin
from rest_framework.response import Response
from rest_framework import status


class CategoriesView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class QuestionViewSet(CustomCreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = (
            queryset.order_by("title"))
        return queryset


class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)
    pagination_class = None

    def create(self, request, *args, **kwargs):
        """ Override create method to handle list of answers """
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SkillTestViewSet(CustomCreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    queryset = SkillTest.objects.all()
    serializer_class = SkillTestSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = (
            queryset.prefetch_related("questions").order_by("-creation_time"))
        return queryset
