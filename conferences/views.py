from django_filters import rest_framework as filters
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .filters import *
from .models import *
from .serializers import *


class ConferenceSessionListAPIView(generics.ListAPIView):
    queryset = ConferenceSession.objects.all()
    serializer_class = ConferenceSessionSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ConferenceSessionFilter


class FilterOptionsAPIView(APIView):
    """
    Get filter options for the conference session list view.
    """

    def get(self, request, *args, **kwargs):
        categories = SessionCategory.objects.all()
        dates = ConferenceSession.objects.dates("start_time", "day", order="ASC")
        language_choices = [
            {"value": choice[0], "label": choice[1]} for choice in LANGUAGE_CHOICES
        ]
        category_serializer = SessionCategorySerializer(categories, many=True)
        return Response(
            {
                "categories": category_serializer.data,
                "languages": language_choices,
                "dates": [date.strftime("%Y-%m-%d") for date in dates],
            },
            status=status.HTTP_200_OK,
        )


class SponsorListAPIView(generics.ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
