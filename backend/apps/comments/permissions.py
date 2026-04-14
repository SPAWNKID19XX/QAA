from rest_framework.permissions import BasePermission


class IsCommentAuthorOrAdmin(BasePermission):
    """Only the comment author or an admin may delete a comment."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        return obj.author == request.user
