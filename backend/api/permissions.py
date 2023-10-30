from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """Права доступа для администратора или только чтение."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user
                and request.user.is_superuser)


class IsAdminOrAuthor(BasePermission):
    """Права доступа для администратора и автора поста."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user == obj.author
                or request.user.is_superuser)
