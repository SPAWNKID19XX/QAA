import logging

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from apps.projects.models import Project
from apps.projects.serializers import ProjectSerializer
from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer

logger = logging.getLogger(__name__)


class GlobalSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        q = request.query_params.get("q", "").strip()
        if q is None:
            return Response(
                {"detail": "Search query parameter 'q' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user

        # Scope projects to those the user can access
        if user.is_admin:
            accessible_projects = Project.objects.all()
        else:
            accessible_projects = (
                Project.objects.filter(owner=user) | Project.objects.filter(members=user)
            ).distinct()

        matched_projects = accessible_projects.filter(
            Q(title__icontains=q) | Q(description__icontains=q)
        ).distinct()

        matched_tasks = Task.objects.filter(
            project__in=accessible_projects
        ).filter(
            Q(title__icontains=q) | Q(description__icontains=q)
        ).distinct()

        return Response(
            {
                "projects": ProjectSerializer(
                    matched_projects, many=True, context={"request": request}
                ).data,
                "tasks": TaskSerializer(
                    matched_tasks, many=True, context={"request": request}
                ).data,
            }
        )
