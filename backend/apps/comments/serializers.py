from rest_framework import serializers

from apps.accounts.serializers import UserPublicSerializer

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "task", "author", "body", "created_at"]
        read_only_fields = ["id", "task", "author", "created_at"]
