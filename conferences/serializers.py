from rest_framework import serializers
from .models import *


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
