from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.paginators import PageLimitPagination
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from api.serializers import (CustomRecipeSerializer, IngredientSerializer,
                             RecipeSerializer, TagSerializer)
from recipes.models import (Favorite, Ingredient, IngredientRecipe,
                            Recipe, ShoppingCart, Tag)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, IngredientFilter,)
    search_fields = ("^name",)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = RecipeFilter
    pagination_class = PageLimitPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["POST", "DELETE"],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == "POST":
            serializer = CustomRecipeSerializer(recipe)
            Favorite.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            obj_to_delete = get_object_or_404(Favorite, user=request.user,
                                              recipe=recipe)
            obj_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            "errors": "Можно использовать только методы Post и Delete"},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST", "DELETE"],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == "POST":
            serializer = CustomRecipeSerializer(recipe)
            ShoppingCart.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            obj_to_delete = get_object_or_404(ShoppingCart, user=request.user,
                                              recipe=recipe)
            obj_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            "errors": "Можно использовать только методы Post и Delete"},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        if not user.shoppingcart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ingredients = (
            IngredientRecipe.objects.filter(recipe__shoppingcart__user=user)
            .values("ingredient__name",
                    "ingredient__measurement_unit",)
            .order_by("ingredient__name")
            .annotate(total=Sum("amount")))
        shopping_list_content = "Список покупок:\n\n"
        shopping_list_content += '\n'.join([
            f'{ingredient["ingredient__name"]} - {ingredient["total"]} '
            f'{ingredient["ingredient__measurement_unit"]}'
            for ingredient in ingredients])
        response = HttpResponse(shopping_list_content,
                                content_type="text/plain")
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.txt"')
        return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly, )
