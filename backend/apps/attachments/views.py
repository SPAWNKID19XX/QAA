import logging

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.tasks.models import Task

from .models import Attachment
from .permissions import IsUploaderOrProjectOwner
from .serializers import AttachmentSerializer

logger = logging.getLogger(__name__)


class AttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = AttachmentSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_permissions(self):
        if self.action == "destroy":
            return [IsAuthenticated(), IsUploaderOrProjectOwner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        task_pk = self.kwargs.get("task_pk")
        if task_pk:
            return Attachment.objects.filter(task_id=task_pk)
        return Attachment.objects.filter(uploaded_by=self.request.user)

    def get_object(self):
        obj = get_object_or_404(Attachment, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        task_pk = self.kwargs.get("task_pk")
        task = get_object_or_404(Task, pk=task_pk)

        # Only project members may upload
        if not request.user.is_admin and not task.project.is_member(request.user):
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(task=task, uploaded_by=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.file.delete(save=False)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
