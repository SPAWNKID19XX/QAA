from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers as nested_routers

from apps.tasks.urls import flat_router as tasks_router

from .views import AttachmentViewSet

# Nested: /api/tasks/{task_pk}/attachments/
tasks_nested_router = nested_routers.NestedDefaultRouter(
    tasks_router, r"tasks", lookup="task"
)
tasks_nested_router.register(r"attachments", AttachmentViewSet, basename="task-attachments")

# Flat delete: /api/attachments/{pk}/
flat_router = DefaultRouter()
flat_router.register(r"attachments", AttachmentViewSet, basename="attachment")

urlpatterns = [
    path("", include(tasks_nested_router.urls)),
    path("", include(flat_router.urls)),
]
