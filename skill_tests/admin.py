from django.contrib import admin
from skill_tests.models import Category, Question, SkillTest, TestStatistic
from django.contrib.admin import ModelAdmin


class AdminBase(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    list_display_links = ("pk", "title")


class CategoryAdmin(AdminBase):
    list_display = ("pk", "title")


class QuestionAdmin(AdminBase):
    list_display = ("pk", "title")


class SkillTestAdmin(AdminBase):
    list_display = ("pk", "title")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(SkillTest, SkillTestAdmin)
