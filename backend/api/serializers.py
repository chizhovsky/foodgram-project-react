from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        ReadOnlyField, SerializerMethodField)

from recipes.models import (Favorite, Ingredient, IngredientRecipe,
                            Recipe, ShoppingCart, Tag)
from users.models import Follow, User


class CustomUserSerializer(UserSerializer):
    """Сериализатор для пользователей."""

    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "first_name",
                  "last_name", "email", "is_subscribed", )

    def get_is_subscribed(self, obj):
        return(
            self.context["request"].user.is_authenticated
            and Follow.objects.filter(
            user=self.context["request"].user, author=obj).exists())


class CreateUserSerializer(UserCreateSerializer):
    """Сериализатор для создания нового пользователя."""

    class Meta:
        model = User
        fields = ("id", "username", "password", "first_name",
                  "last_name", "email", )


class IngredientSerializer(ModelSerializer):
    """Сериализатор для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = "__all__"


class TagSerializer(ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientRecipeSerializer(ModelSerializer):
    """Сериализатор для связи ингредиентов и рецептов."""

    id = ReadOnlyField(source="ingredient.id")
    name = ReadOnlyField(source="ingredient.name")
    measurement_unit = ReadOnlyField(source="ingredient.measurement_unit")
    amount = ReadOnlyField()

    class Meta:
        model = IngredientRecipe
        fields = ("id", "name", "measurement_unit", "amount", )


class RecipeSerializer(ModelSerializer):
    """Сериализатор для получения рецептов."""

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

    def get_ingredients(self, obj):
        ingredients = IngredientRecipeSerializer.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(ingredients, many=True).data


class RecipeCreateSerializer(RecipeSerializer):
    """Сериализатор для создания и удаления рецептов."""

    image = Base64ImageField()
    cooking_time = IntegerField()

    class Meta:
        model = Recipe
    fields = ("id", "name", "tags", "ingredients",
              "author", "image", "text", "cooking_time", )

    def create_ingredients(self, ingredients, recipe):
        """Функция для добавления ингредиентов."""

        IngredientRecipe.objects.bulk_create([
            IngredientRecipe(
                ingredient=ingredient["id"],
                recipe=recipe,
                amount=ingredient["amount"],) for ingredient in ingredients])

    def create(self, validated_data):
        """Функция для создания рецепта."""

        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        return recipe

    def update(self, recipe, validated_data):
        """Функция для обновления рецепта."""

        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        ingredients_recipe = IngredientRecipe.objects.filter(recipe=recipe)
        ingredients_recipe.delete()
        self.create_ingredients(recipe, ingredients)
        recipe.tags.set(tags)
        return super().update(recipe, validated_data)

    def to_representation(self, instance):
        """Функция для отображения рецепта."""

        return RecipeSerializer(instance, context={
            "request": self.context.get("request")}).data

    def validate(self):
        """Функция для валидации данных."""
        ...


class RecipeFollowSerializer(ModelSerializer):
    """Сериализатор для добавления рецепта в избранное."""

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "text", "cooking_time")


class FollowSerializer(ModelSerializer):
    """Сериализатор для подписок."""

    email = ReadOnlyField(source="author.email")
    id = ReadOnlyField(source="author.id")
    username = ReadOnlyField(source="author.username")
    first_name = ReadOnlyField(source="author.first_name")
    last_name = ReadOnlyField(source="author.last_name")
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField(read_only=True)
    is_subscribed = SerializerMethodField()

    class Meta:
        model = Follow
        fields = ("email", "id", "username", "first_name",
                  "last_name", "recipes", "recipes_count", "is_subscribed", )

    def get_recipes(self, obj):
        return Recipe.objects.filter(author=obj.author).count()

    def get_is_subscribed(self, obj):
        return obj.author.follower.filter(user=obj.user).exists()
