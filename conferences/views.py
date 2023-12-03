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
        rooms = Room.objects.order_by("sort_order")
        categories = SessionCategory.objects.all()
        speakers = Speaker.objects.all()
        dates = ConferenceSession.objects.dates("start_time", "day", order="ASC")
        language_choices = [
            {"value": choice[0], "label": choice[1]} for choice in LANGUAGE_CHOICES
        ]
        room_serializer = RoomSerializer(rooms, many=True)
        category_serializer = SessionCategorySerializer(categories, many=True)
        speaker_serializer = SpeakerSerializer(speakers, many=True)
        return Response(
            {
                "rooms": room_serializer.data,
                "categories": category_serializer.data,
                "speakers": speaker_serializer.data,
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
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SpeakerFilter


class SearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get("search_query", "")
        speakers = Speaker.objects.filter(name__icontains=search_query).order_by("name")
        conference_sessions = ConferenceSession.objects.filter(
            models.Q(title_en__icontains=search_query)
            | models.Q(title_ja__icontains=search_query)
        ).order_by("title_en")

        # Group speakers by the first letter of their names
        grouped_speakers = {}
        for speaker in speakers:
            first_letter = speaker.name[0].upper()
            grouped_speakers.setdefault(first_letter, []).append(
                SpeakerSerializer(speaker).data
            )

        # Group conference sessions by the first letter of their titles
        grouped_sessions = {}
        for session in conference_sessions:
            first_letter = (
                session.title_en[0].upper()
                if session.title_en
                else session.title_ja[0].upper()
            )
            grouped_sessions.setdefault(first_letter, []).append(
                ConferenceSessionReadSerializer(session).data
            )

        return Response(
            {
                "speakers": grouped_speakers,
                "conference_sessions": grouped_sessions,
            },
            status=status.HTTP_200_OK,
        )
