import django_filters

from .models import Project


class ProjectFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Project.STATUS_CHOICES)

    class Meta:
        model = Project
        fields = ["status"]
