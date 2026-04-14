from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers as nested_routers

from apps.projects.urls import router as projects_router

from .views import TaskViewSet

# Nested router: /api/projects/{project_pk}/tasks/
projects_nested_router = nested_routers.NestedDefaultRouter(
    projects_router, r"projects", lookup="project"
)
projects_nested_router.register(r"tasks", TaskViewSet, basename="project-tasks")

# Flat router: /api/tasks/{pk}/
flat_router = DefaultRouter()
flat_router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("", include(projects_nested_router.urls)),
    path("", include(flat_router.urls)),
]
