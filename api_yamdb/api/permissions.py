from rest_framework import permissions
# from rest_framework.permissions import BasePermission


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.role == 'admin'


# class IsModeratorUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.is_moderator
#
#     def has_object_permission(self, request, view, obj):
#         if obj.role == 'moderator':
#             return True
#         return False


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        print('Helllllllll')
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'admin'
        # return obj.role == 'admin'


# class ReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.method in permissions.SAFE_METHODS

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsAdminOrModeratorOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.role == 'admin'
                or request.role == 'moderator'
                or obj.username == request.username)


class IsAdminOrReadOnlyTwo(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated and request.user.role == 'admin'
            )
        )


class ReviewCommentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or request.user.username == obj.author.username)
