from djoser.serializers import UserSerializer
from rest_framework.serializers import (ModelSerializer, ReadOnlyField,
                                        SerializerMethodField)

from recipes.models import (Favorite, Ingredient, IngredientRecipe,
                            Recipe, ShoppingCart)
from users.models import User


class CustomUserSerializer(UserSerializer):
    """Сериализатор для пользователей."""

    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "first_name",
                  "last_name", "email", "is_subscribed", )

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        return (user.is_authenticated and
                user.subscriber.filter(author=obj).exists())


class IngredientSerializer(ModelSerializer):
    """Сериализатор для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = "__all__"


class TagSerializer(ModelSerializer):
    ...


class IngredientRecipeSerializer(ModelSerializer):
    """Сериализатор для связи ингредиентов и рецептов."""

    id = ReadOnlyField(source="ingredient.id")
    name = ReadOnlyField(source="ingredient.name")
    measurement_unit = ReadOnlyField(source="ingredient.measurement_unit")

    class Meta:
        model = IngredientRecipe
        fields = ("id", "name", "measurement_unit", "amount", )


class RecipeSerializer(ModelSerializer):
    """Сериализатор для рецептов."""

    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientRecipeSerializer(many=True, read_only=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ("id", "name", "tags", "ingredients", "author",
                  "is_favorited", "is_in_shopping_cart", "image",
                  "text", "cooking_time", )

    def get_is_favorited(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=user, recipe=obj).exists()



