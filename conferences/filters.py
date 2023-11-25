import django_filters
from .models import *


class ConferenceSessionFilter(django_filters.FilterSet):
    search_query = django_filters.CharFilter(method="filter_search_query")

    class Meta:
        model = ConferenceSession
        fields = {
            "language": ["exact"],
            "category": ["exact"],
            "start_time": ["date__exact"],
        }

    def filter_search_query(self, queryset, name, value):
        return queryset.filter(
            models.Q(title_en__icontains=value) | models.Q(title_ja__icontains=value)
        )