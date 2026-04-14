from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.accounts.serializers import UserPublicSerializer

from .models import Project, ProjectMember

User = get_user_model()


class ProjectMemberSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = ProjectMember
        fields = ["id", "user", "joined_at"]
        read_only_fields = fields


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(read_only=True)
    project_members = ProjectMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "status",
            "owner",
            "project_members",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "owner", "project_members", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class AddMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        if not User.objects.filter(pk=value).exists():
            raise serializers.ValidationError("User not found.")
        return value
