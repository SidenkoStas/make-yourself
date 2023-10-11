from django.contrib import admin
from blog.models import Category, Post, Comment, View
from mptt.admin import DraggableMPTTAdmin

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


class CommentAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', "pk", "post", "author")
    list_display_links = ("pk", "post")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(View)
