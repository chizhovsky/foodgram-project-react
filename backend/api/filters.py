from django_filters.rest_framework import (AllValuesFilter, AllValuesMultipleFilter,
                                            BooleanFilter, FilterSet)
from rest_framework.filters import SearchFilter

from recipes.models import Recipe


class IngredientFilter(SearchFilter):
    """Фильтр для ингредиентов."""

    search_param = "name"


class RecipeFilter(FilterSet):
    """Фильтр для рецептов."""
    author = AllValuesFilter(field_name="author")
    tags = AllValuesMultipleFilter(field_name="tags__slug")
    is_favorited = BooleanFilter(method="get_is_favorited")
    is_in_shopping_cart = BooleanFilter(method="get_is_in_shopping_cart")

    class Meta:
        model = Recipe
        fields = ("author", "tags", "is_favorited", "is_in_shopping_cart")

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorite__user=user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shoppingcart__user=user)
        return queryset
