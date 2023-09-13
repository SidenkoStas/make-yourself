from django.contrib import admin
from blog.models import Category, Post, Comment


class AdminBase(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    list_display_links = ("pk", "title")


class CategoryAdmin(AdminBase):
    list_display = ("pk", "title")


class PostAdmin(AdminBase):
    list_display = (
        "pk", "title", "author", "creation_date", "is_published"
    )
    list_filter = ("is_published", )


class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "post", "author")
    list_display_links = ("pk", "post")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
