import logging

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import ProjectFilter
from .models import Project, ProjectMember
from .permissions import IsProjectOwner, IsProjectOwnerOrReadOnly
from .serializers import AddMemberSerializer, ProjectMemberSerializer, ProjectSerializer

logger = logging.getLogger(__name__)
User = get_user_model()


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    filterset_class = ProjectFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Project.objects.all().distinct()
        return Project.objects.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsProjectOwnerOrReadOnly()]
        if self.action in ("add_member", "remove_member"):
            return [IsAuthenticated(), IsProjectOwner()]
        return [IsAuthenticated()]

    def get_object(self):
        obj = get_object_or_404(Project, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=True, methods=["post"], url_path="members")
    def add_member(self, request, pk=None):
        project = self.get_object()
        serializer = AddMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data["user_id"]
        user = get_object_or_404(User, pk=user_id)

        if project.owner == user:
            return Response(
                {"detail": "User is already the project owner."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        membership, created = ProjectMember.objects.get_or_create(project=project, user=user)
        if not created:
            return Response(
                {"detail": "User is already a member of this project."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(ProjectMemberSerializer(membership).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"], url_path=r"members/(?P<user_id>\d+)")
    def remove_member(self, request, pk=None, user_id=None):
        project = self.get_object()
        user = get_object_or_404(User, pk=user_id)
        deleted, _ = ProjectMember.objects.filter(project=project, user=user).delete()
        if not deleted:
            return Response({"detail": "Member not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
