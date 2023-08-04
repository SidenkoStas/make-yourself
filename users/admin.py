from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Notification, CustomUser
from django.utils.safestring import mark_safe


class CustomUserAdmin(UserAdmin):
    """Добавление в админку сайта собственной модели и форму регистрации
       пользователей, настройка отображения полей в админке.
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = (
        *UserAdmin.fieldsets,
        (None, {"fields": ("photo", "bio", "notifications")})
    )
    list_display = [
        "id", "username", "email", "get_html_photo", "get_bio",
        "get_notifications"
    ]
    list_display_links = ["id", "username"]

    def get_notifications(self, obj):
        return "\n".join([i.notification for i in obj.notifications.all()])

    def get_bio(self, obj):
        """
        Если биография длиннее 100 символов - возвращает обрезанную версию.
        """
        if len(obj.bio) > 100:
            return mark_safe(f"{obj.bio[:100]}...")

    def get_html_photo(self, obj):
        """
        Проверяет есть ли фото, если есть - возвращает HTML элемент
        для отображения миниатюры.
        """
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width=50")

    get_notifications.short_description = "Уведомления"
    get_bio.short_description = "Биография"
    get_html_photo.short_description = "Фото миниатюра"


class NotificationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["notification"]}


admin.site.register(Notification, NotificationAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
