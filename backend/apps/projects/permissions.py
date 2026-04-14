from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProjectOwnerOrReadOnly(BasePermission):
    """
    Project detail: members (including owner) may read.
    Only the owner (or admin) may write/delete.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        if request.method in SAFE_METHODS:
            return obj.is_member(request.user)
        return obj.owner == request.user


class IsProjectOwner(BasePermission):
    """Only the project owner (or admin) may perform the action."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        return obj.owner == request.user
