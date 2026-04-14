from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProjectMember(BasePermission):
    """
    Allows access only to members (including owner) of the task's project.
    Admins bypass all checks.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        project = obj.project
        if request.method in SAFE_METHODS:
            return project.is_member(request.user)
        # Write: creator or project owner may modify/delete
        return obj.created_by == request.user or project.owner == request.user
