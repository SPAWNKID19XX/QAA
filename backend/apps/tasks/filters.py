import django_filters

from .models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Task.STATUS_CHOICES)
    priority = django_filters.CharFilter(field_name="status")
    assignee = django_filters.NumberFilter(field_name="assignee__id")

    class Meta:
        model = Task
        fields = ["status", "priority", "assignee"]
