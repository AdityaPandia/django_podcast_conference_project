from rest_framework import serializers
from .models import *

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields = ('id','name','url','pic_url')

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ('name', 'description', 'audio_url','url','podcast')

class PodcastSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = Podcast
        fields = ('id', 'name', 'description', 'episode_amount', 'url','tags','episodes')


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = (
            "id",
            "name",
            "bio",
            "tag_line",
            "profile_pic_url",
            "created_at",
            "updated_at",
        )


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "id",
            "title_en",
            "title_ja",
            "sort_order",
            "created_at",
            "updated_at",
        )


class SessionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionCategory
        fields = ("id", "title_en", "title_ja", "created_at", "updated_at")


class ConferenceSessionReadSerializer(serializers.ModelSerializer):
    speakers = SpeakerSerializer(many=True)
    room = RoomSerializer()
    category = SessionCategorySerializer()
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = ConferenceSession
        fields = (
            "id",
            "title_en",
            "title_ja",
            "description_en",
            "description_ja",
            "target_audience",
            "video_url",
            "slide_url",
            "message_en",
            "message_ja",
            "speakers",
            "room",
            "category",
            "start_time",
            "end_time",
            "duration",
            "language",
            "session_type",
            "is_service_session",
            "interpretation_target",
            "is_liked",
            "likes_count",
            "created_at",
            "updated_at",
        )

    def get_is_liked(self, obj):
        device_id = self.context.get("device_id")
        if device_id:
            return obj.session_likes.filter(device_id=device_id).exists()
        return False

    def get_likes_count(self, obj):
        return obj.session_likes.count()


class ConferenceSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConferenceSession
        fields = (
            "id",
            "title_en",
            "title_ja",
            "description_en",
            "description_ja",
            "target_audience",
            "video_url",
            "slide_url",
            "message_en",
            "message_ja",
            "speakers",
            "room",
            "category",
            "start_time",
            "end_time",
            "duration",
            "language",
            "session_type",
            "is_service_session",
            "interpretation_target",
            "created_at",
            "updated_at",
        )


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = (
            "id",
            "title",
            "logo_url",
            "website_url",
            "plan",
            "created_at",
            "updated_at",
        )
