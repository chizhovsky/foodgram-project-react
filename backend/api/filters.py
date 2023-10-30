from django_filters.rest_framework import FilterSet
from rest_framework.filters import SearchFilter


class IngredientFilter(SearchFilter):
    """Фильтр для ингредиентов."""

    search_param = "name"


class RecipeFilter(FilterSet):
    """Фильтр для рецептов."""
    ...

