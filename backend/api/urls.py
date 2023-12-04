from django.urls import include, path
from rest_framework import routers

from api.views import IngredientViewSet, RecipeViewSet, TagViewSet
from users.views import CustomUserViewSet

app_name = "api"

router = routers.DefaultRouter()

router.register("ingredients", IngredientViewSet, basename="ingredients")
router.register("recipes", RecipeViewSet, basename="recipes")
router.register("tags", TagViewSet, basename="tags")
router.register("users", CustomUserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls), ),
    path("auth/", include("djoser.urls.authtoken")), ]
