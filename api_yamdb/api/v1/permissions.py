from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ только пользователям с правами администратора
    или для чтения.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated and request.user.is_admin
            )
        )


class ReviewCommentPermission(permissions.BasePermission):
    """
    Разрешает доступ для чтения или для редактирования пользователям
    с правами администратора, модератора или автора.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or request.user.username == obj.author.username)
