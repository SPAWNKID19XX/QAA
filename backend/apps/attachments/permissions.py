from rest_framework.permissions import BasePermission


class IsUploaderOrProjectOwner(BasePermission):
    """Only the uploader or the project owner (or admin) may delete an attachment."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        return (
            obj.uploaded_by == request.user
            or obj.task.project.owner == request.user
        )
