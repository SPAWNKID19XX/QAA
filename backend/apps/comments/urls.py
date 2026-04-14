from django.urls import path, include
from rest_framework_nested import routers as nested_routers

from apps.tasks.urls import flat_router as tasks_router

from .views import CommentViewSet

# Nested: /api/tasks/{task_pk}/comments/
tasks_nested_router = nested_routers.NestedDefaultRouter(
    tasks_router, r"tasks", lookup="task"
)
tasks_nested_router.register(r"comments", CommentViewSet, basename="task-comments")

# Flat delete: /api/comments/{pk}/
from rest_framework.routers import DefaultRouter

flat_router = DefaultRouter()
flat_router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(tasks_nested_router.urls)),
    path("", include(flat_router.urls)),
]
