from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель для пользователя."""

    username = models.CharField(
        max_length=150,
        verbose_name="Логин",
        unique=True,
        default="Spider-man",)
    password = models.CharField(
        max_length=150,
        verbose_name="Пароль",
        default="password",)
    first_name = models.CharField(
        max_length=150,
        verbose_name="Имя пользователя",
        default="Peter",)
    last_name = models.CharField(
        max_length=150,
        verbose_name="Фамилия пользователя",
        default="Parker",)
    email = models.EmailField(
        max_length=254,
        verbose_name="Электронная почта",
        unique=True,
        default="example@mail.com",)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", ]

    class Meta:
        ordering = ['username', ]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель для подписок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Подписчик",
        related_name="follower",)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name="author",)

    class Meta:
        ordering = ['user',]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=("user", "author"),
                name="unique_follow"), ]

    def __str__(self):
        return f"{self.user} подписан на {self.author}"
