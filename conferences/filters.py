import django_filters
from .models import *


class ConferenceSessionFilter(django_filters.FilterSet):
    search_query = django_filters.CharFilter(method="filter_search_query")

    class Meta:
        model = ConferenceSession
        fields = {
            "language": ["in"],
            "category": ["in"],
            "room": ["in"],
            "start_time": ["date__in"],
            "id": ["in"],
        }

    def filter_search_query(self, queryset, name, value):
        return queryset.filter(
            models.Q(title_en__icontains=value) | models.Q(title_ja__icontains=value)
        )


class SpeakerFilter(django_filters.FilterSet):
    search_query = django_filters.CharFilter(method="filter_search_query")

    class Meta:
        model = Speaker
        fields = ("search_query",)

    def filter_search_query(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
