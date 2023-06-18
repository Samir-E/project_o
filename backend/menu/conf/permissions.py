from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow admin users to edit objects
    to edit / delete it. Assumes the model instance has a
    `is_staff` attribute
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
