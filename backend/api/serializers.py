from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        PrimaryKeyRelatedField,
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
        fields = ("id", "name", "measurement_unit",)
        read_only_fields = ("id", "name", "measurement_unit",)


class TagSerializer(ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tag
        fields = "__all__"


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
    ingredients = IngredientRecipeSerializer(
        many=True,
        read_only=True,
        source="ingredientrecipe")
    image = Base64ImageField(required=True)
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
        ingredients = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(ingredients, many=True).data

    def create_ingredients(self, ingredients, recipe):
        """Функция для добавления ингредиентов."""

        IngredientRecipe.objects.bulk_create([
            IngredientRecipe(
                ingredient_id=ingredient.get("id"),
                recipe=recipe,
                amount=ingredient["amount"], ) for ingredient in ingredients])

    def validate(self, data):
        """Функция для валидации данных."""

        user = self.context.get("request").user
        name = data["name"]
        ingredients = self.initial_data["ingredients"]
        if name == "":
            raise ValidationError("Название рецепта не должно быть пустым!")
        if self.context.get("request").method == "POST" and Recipe.objects.filter(
                author=user, name=name).exists():
            raise ValidationError("Рецепт с таким названием уже существует!")
        if not ingredients:
            raise ValidationError("Добавьте как минимум один ингредиент!")
        ingredients_amount = []
        for i in ingredients:
            ingredient = get_object_or_404(Ingredient, id=i["id"])
            if ingredient in ingredients_amount:
                raise ValidationError("Нельзя добавлять одинаковые ингредиенты!")
            ingredients_amount.append(ingredient)
        data["ingredients"] = ingredients
        tags = self.initial_data["tags"]
        if not tags:
            raise ValidationError("Выберите хотя бы один тег!")
        return data

    def create(self, validated_data):
        """Функция для создания рецепта."""

        ingredients = validated_data.pop("ingredients")
        tags = self.initial_data.get("tags")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, recipe, validated_data):
        """Функция для обновления рецепта."""

        recipe.tags.clear()
        recipe.tags.set(self.initial_data.get("tags"))
        IngredientRecipe.objects.filter(recipe=recipe).all().delete()
        ingredients = validated_data.pop("ingredients")
        self.create_ingredients(ingredients, recipe)
        return super().update(recipe, validated_data)


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
