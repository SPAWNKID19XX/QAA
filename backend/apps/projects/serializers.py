from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.accounts.serializers import UserPublicSerializer, OwnerProjectSerializer

from .models import Project, ProjectMember

User = get_user_model()


class ProjectMemberSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = ProjectMember
        fields = ["id", "user", "joined_at"]
        read_only_fields = fields


class ProjectSerializer(serializers.ModelSerializer):
    owner = OwnerProjectSerializer(read_only=True)
    project_members = ProjectMemberSerializer(many=True, read_only=True)
    members_count = serializers.IntegerField(source="project_members.count", read_only=True)


    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop("exclude_fields", None)
        super().__init__(*args, **kwargs)

        if exclude_fields:
            for field in exclude_fields:
                self.fields.pop(field, None)

    class Meta:
        model = Project
        fields = "__all__"
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
