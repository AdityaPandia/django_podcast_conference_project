from django.urls import path
from .views import *


app_name = "resume"

urlpatterns = [
    path(
        "conferences/sessions/",
        ConferenceSessionListAPIView.as_view(),
        name="conference-session-list",
    ),
    path(
        "conferences/sessions/filters/",
        FilterOptionsAPIView.as_view(),
        name="conference-session-filters",
    ),
    path(
        "conferences/speakers/",
        SpeakerListAPIView.as_view(),
        name="speaker-list",
    ),
    path(
        "conferences/sponsors/",
        SponsorListAPIView.as_view(),
        name="sponsor-list",
    ),
]
