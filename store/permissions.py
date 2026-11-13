from rest_framework.permissions import BasePermission


class IsVendor(BasePermission):
    """Allow access only to authenticated vendors."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'userprofile')
            and request.user.userprofile.role == 'vendor'
        )
