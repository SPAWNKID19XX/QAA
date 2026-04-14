from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.accounts.serializers import UserPublicSerializer

from .models import Task

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    created_by = UserPublicSerializer(read_only=True)
    assignee = UserPublicSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="assignee",
        allow_null=True,
        required=False,
        write_only=True,
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "project",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "assignee_id",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "project", "created_by", "created_at", "updated_at"]

    def validate(self, attrs):
        assignee = attrs.get("assignee")
        # On update, project comes from the instance; on create, from the view context.
        project = getattr(self.instance, "project", None) or self.context.get("project")

        if assignee and project:
            is_member = (
                project.owner == assignee
                or project.members.filter(pk=assignee.pk).exists()
            )
            if not is_member:
                raise serializers.ValidationError(
                    {"assignee_id": "Assignee must be a member of the project."}
                )
        return attrs
