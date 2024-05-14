from django.urls import path
from .views import ConferenceSessionListAPIView, FilterOptionsAPIView, PodcastListAPIView, EpisodeListAPIView, AuthorListAPIView, SearchAPIView, SessionLikeAPIView, SpeakerListAPIView, SponsorListAPIView


app_name = "resume"

urlpatterns = [
  path('authors/',AuthorListAPIView.as_view(),name='author-list'),
    path('podcasts/', PodcastListAPIView.as_view(), name='podcast-list'),
    path('podcasts/<str:podcast_id>/episodes/', EpisodeListAPIView.as_view(), name='episode-list'),
    
    path(
        "conferences/sessions/",
        ConferenceSessionListAPIView.as_view(),
        name="conference-session-list",
    ),
    path(
        "conferences/sessions/<int:pk>/like/",
        SessionLikeAPIView.as_view(),
        name="session-like",
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
        "conferences/search/",
        SearchAPIView.as_view(),
        name="search",
    ),
    path(
        "conferences/sponsors/",
        SponsorListAPIView.as_view(),
        name="sponsor-list",
    ),
]
