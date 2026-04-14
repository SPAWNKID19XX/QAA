from rest_framework import serializers

from apps.accounts.serializers import UserPublicSerializer

from .models import Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    uploaded_by = UserPublicSerializer(read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = ["id", "task", "uploaded_by", "file", "file_url", "filename", "uploaded_at"]
        read_only_fields = ["id", "task", "uploaded_by", "filename", "uploaded_at", "file_url"]
        extra_kwargs = {"file": {"write_only": True}}

    def get_file_url(self, obj):
        request = self.context.get("request")
        if request and obj.file:
            return request.build_absolute_uri(obj.file.url)
        return None

    def create(self, validated_data):
        validated_data["filename"] = validated_data["file"].name
        return super().create(validated_data)
