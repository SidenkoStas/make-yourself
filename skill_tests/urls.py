from django.urls import path, include
from skill_tests.views import CategoriesView, QuestionViewSet, SkillTestViewSet
from rest_framework.routers import DefaultRouter


app_name = "skill_test"
router = DefaultRouter()
router.register("questions", QuestionViewSet, basename="question")
router.register("testing", SkillTestViewSet, basename="testing")

urlpatterns = [
    path("categories/", CategoriesView.as_view(), name="categories"),
    path("", include(router.urls)),
]
