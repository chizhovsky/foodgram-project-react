from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """Права доступа для администратора или только чтение."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_superuser)


class IsAuthorOrReadOnly(BasePermission):
    """Права доступа для автора поста или только чтение."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
