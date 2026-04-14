import logging

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.projects.models import Project

from .filters import TaskFilter
from .models import Task
from .permissions import IsProjectMember
from .serializers import TaskSerializer

logger = logging.getLogger(__name__)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filterset_class = TaskFilter

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsProjectMember()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        project_pk = self.kwargs.get("project_pk")

        if project_pk:
            project = get_object_or_404(Project, pk=project_pk)
            if not user.is_admin and not project.is_member(user):
                return Task.objects.none()
            return Task.objects.filter(project=project)

        # Flat URL — return tasks from projects the user can access
        if user.is_admin:
            return Task.objects.all()
        accessible_projects = Project.objects.filter(owner=user) | Project.objects.filter(members=user)
        return Task.objects.filter(project__in=accessible_projects)

    def get_object(self):
        obj = get_object_or_404(Task, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        project_pk = self.kwargs.get("project_pk")
        project = get_object_or_404(Project, pk=project_pk)

        if not request.user.is_admin and not project.is_member(request.user):
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(
            data=request.data,
            context={**self.get_serializer_context(), "project": project},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(project=project, created_by=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        project_pk = self.kwargs.get("project_pk")
        if project_pk:
            context["project"] = get_object_or_404(Project, pk=project_pk)
        elif self.kwargs.get("pk"):
            task = Task.objects.filter(pk=self.kwargs["pk"]).first()
            if task:
                context["project"] = task.project
        return context
