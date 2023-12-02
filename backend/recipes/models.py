from django.db import models
from django.core.validators import MinValueValidator

from users.models import User


class Ingredient(models.Model):
    """Модель для ингредиентов."""

    name = models.CharField(
        max_length=200,
        verbose_name="Ингредиент",)
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name="Единица измерения")

    class Meta:
        ordering = ["name",]
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель для тегов."""

    name = models.CharField(
        max_length=200,
        verbose_name="Тег",)
    color = models.CharField(
        max_length=7,
        null=True,
        blank=True,
        verbose_name="Цвет (hex)",)
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Slug",)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель для рецептов."""

    name = models.CharField(
        max_length=200,
        verbose_name="Рецепт",)
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Теги",)
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientRecipe",
        verbose_name="Ингредиенты")
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,)
    image = models.ImageField(
        verbose_name="Изображение",
        upload_to='images/',)
    text = models.TextField(
        verbose_name="Описание")
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления",
        validators=[MinValueValidator(1,
            message="Время приготовления не должно быть меньше одной минуты.")])

    class Meta:
        ordering = ['-id']
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """Модель для связи ингредиентов и рецептов."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент",)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredientrecipe",
        verbose_name="Рецепт",)
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество",
        validators=[MinValueValidator(1,
            message="Количество ингредиентов должно быть не меньше одного.")])

    class Meta:
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецепте"
        constraints = [
            models.UniqueConstraint(
                fields=("recipe", "ingredient"),
                name="unique_ingredient_recipe"),]


class Favorite(models.Model):
    """Модель для добавления в избранное."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",)

    class Meta:
        verbose_name = "Рецепт в избранном"
        verbose_name_plural = "Рецепты в избранном"
        constraints = [
            models.UniqueConstraint(
                fields=("user", "recipe"),
                name="unique_favorite"), ]

    def __str__(self):
        return f"{self.user}: {self.recipe}"


class ShoppingCart(models.Model):
    """Модель для списка покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь")
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",)

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        constraints = [
            models.UniqueConstraint(
                fields=("user", "recipe"),
                name="unique_shoppingcart"), ]
