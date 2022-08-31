from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ только пользователям с правами администратора
    или для чтения.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated and request.user.role == 'admin'
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
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or request.user.username == obj.author.username)
