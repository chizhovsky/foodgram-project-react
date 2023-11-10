from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.paginators import PageLimitPagination
from api.permissions import IsAdminOrAuthor, IsAdminOrReadOnly
from api.serializers import (IngredientSerializer, RecipeCreateSerializer,
                             RecipeFollowSerializer, RecipeSerializer, TagSerializer)
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (IngredientFilter,)
    search_fields = ("^name",)


class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для рецептов."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAdminOrAuthor,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = PageLimitPagination

    def get_serializer_class(self):
        method = self.request.method
        if method == "POST" or method == "PATCH":
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["POST", "DELETE"],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == "POST":
            serializer = RecipeFollowSerializer(recipe)
            Favorite.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            obj_to_delete = get_object_or_404(Favorite, user=request.user,
                                              recipe=recipe)
            obj_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"errors": "Можно использовать только методы Post и Delete"},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST", "DELETE"],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == "POST":
            serializer = RecipeFollowSerializer(recipe)
            ShoppingCart.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            obj_to_delete = get_object_or_404(ShoppingCart, user=request.user,
                                              recipe=recipe)
            obj_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"errors": "Можно использовать только методы Post и Delete"},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ...





class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
