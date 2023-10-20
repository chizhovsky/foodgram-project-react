from django.contrib import admin
from recipes.models import (Favorite, Ingredient, IngredientRecipe,
                            Recipe, ShoppingCart, Tag, TagRecipe)


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe
    min_num = 1
    extra = 5
    verbose_name = 'Тег'
    verbose_name_plural = 'Теги'


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    min_num = 1
    extra = 5
    verbose_name = 'Ингредиент'
    verbose_name_plural = 'Ингредиенты'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Ингредиенты в панели администратора."""
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Теги в панели администратора."""
    list_display = ('name', 'color', 'slug')
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Рецепты в панели администратора."""
    list_display = ('name', 'author', 'add_to_favorite')
    list_filter = ('name', 'author', 'tags')
    inlines = (TagRecipeInline, IngredientRecipeInline)

    @admin.display(description='Счетчик добавлений в избранное')
    def add_to_favorite(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Список покупок в панели администратора."""
    list_display = ('user', 'recipe')
    list_filter = ('user',)
