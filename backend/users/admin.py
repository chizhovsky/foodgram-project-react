from django.contrib import admin

from users.models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Пользователи в панели администратора."""
    list_display = (
        "username",
        "password",
        "first_name",
        "last_name",
        "email",)
    list_filter = ("username", "email",)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Подписки в панели администратора."""
    list_display = ("user", "author",)
    list_filter = ("user", "author",)
