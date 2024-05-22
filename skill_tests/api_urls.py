from django.urls import path, include
from skill_tests.api_views import CategoriesView, QuestionViewSet, SkillTestViewSet, AnswerViewSet
from rest_framework.routers import DefaultRouter


app_name = "api_skill_test"
router = DefaultRouter()
router.register("questions", QuestionViewSet, basename="question")
router.register("answers", AnswerViewSet, basename="answer")
router.register("testing", SkillTestViewSet, basename="testing")


urlpatterns = [
    path("categories/", CategoriesView.as_view(), name="categories"),
    path("", include(router.urls)),
]
