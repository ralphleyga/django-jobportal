import django_filters

from .models import Job

class JobFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Job
        fields = ['country', 'work_environment', 'position']