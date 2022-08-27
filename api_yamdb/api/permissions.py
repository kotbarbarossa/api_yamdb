from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.role == 'admin'


# class IsModeratorUser(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.is_moderator
#
#     def has_object_permission(self, request, view, obj):
#         if obj.role == 'moderator':
#             return True
#         return False


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return obj.role == 'admin'


# class ReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         return request.method in permissions.SAFE_METHODS

class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsAdminOrModeratorOrOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.role == 'admin'
                or request.role == 'moderator'
                or obj.username == request.username)
