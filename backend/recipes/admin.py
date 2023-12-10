from django.contrib import admin
from django.utils.html import format_html

from recipes.models import (Favorite, Ingredient, IngredientRecipe,
                            Recipe, ShoppingCart, Tag)


class IngredientRecipeInline(admin.TabularInline):
    """Вложенная форма для связи Ингредиент - Рецепт."""

    model = IngredientRecipe
    min_num = 1
    extra = 5
    verbose_name = "Ингредиент"
    verbose_name_plural = "Ингредиенты"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Ингредиенты в панели администратора."""

    list_display = ("name", "measurement_unit")
    list_filter = ("name",)
    empty_value_display = "-пусто-"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Теги в панели администратора."""

    list_display = ("name", "colored", "slug")
    list_filter = ("name",)

    @admin.display
    def colored(self, obj):
        return format_html(
            f'<span style="background: {obj.color};'
            f'color: {obj.color}";>___________</span>')

    colored.short_description = "цвет"


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Рецепты в панели администратора."""

    list_display = ("name", "author", "add_to_favorite")
    list_filter = ("name", "author", "tags")
    inlines = [IngredientRecipeInline]

    @admin.display(description="Счетчик добавлений в избранное")
    def add_to_favorite(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Список покупок в панели администратора."""

    list_display = ("user", "recipe")
    list_filter = ("user",)
