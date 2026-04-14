import logging

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.tasks.models import Task

from .models import Comment
from .permissions import IsCommentAuthorOrAdmin
from .serializers import CommentSerializer

logger = logging.getLogger(__name__)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_permissions(self):
        if self.action == "destroy":
            return [IsAuthenticated(), IsCommentAuthorOrAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        task_pk = self.kwargs.get("task_pk")
        if task_pk:
            return Comment.objects.filter(task_id=task_pk)
        return Comment.objects.filter(author=self.request.user)

    def get_object(self):
        obj = get_object_or_404(Comment, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        task_pk = self.kwargs.get("task_pk")
        task = get_object_or_404(Task, pk=task_pk)

        # Only project members may comment
        if not request.user.is_admin and not task.project.is_member(request.user):
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(task=task, author=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
