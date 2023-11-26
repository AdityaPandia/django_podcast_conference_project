from django_filters import rest_framework as filters
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .filters import *
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ConferenceSessionListAPIView(generics.ListCreateAPIView):
    queryset = ConferenceSession.objects.order_by("start_time")
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ConferenceSessionFilter
    # permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return ConferenceSessionReadSerializer
        return ConferenceSessionSerializer

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


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


class SpeakerListAPIView(generics.ListAPIView):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
