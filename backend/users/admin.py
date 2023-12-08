from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from users.models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Пользователи в панели администратора."""
    list_display = (
        "username",
        "password",
        "first_name",
        "last_name",
        "email",
        "followers_count",
        "recipes_count",)
    list_filter = ("username", "email",)

    get_followers_count.short_description = "Подписчики"
    get_recipes_count.short_description = "Рецепты"

    def followers_count(self, obj):
        return obj.follower.count()

    def recipes_count(self, obj):
        return obj.recipes.count()


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Подписки в панели администратора."""
    list_display = ("user", "author",)
    list_filter = ("user", "author",)


admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
