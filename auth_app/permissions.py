from rest_framework.permissions import BasePermission


class EstAdminPermission(BasePermission):
    """
    Custom permission to only allow users with the 'admin' role to access certain views.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has the 'admin' role
        return request.user.role == 'admin'