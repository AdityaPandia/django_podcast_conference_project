from datetime import timedelta
from django.db import models
from django.core.exceptions import ValidationError


LANGUAGE_CHOICES = (
    ("ENGLISH", "English"),
    ("JAPANESE", "Japanese"),
)

SESSION_TYPE_CHOICES = (
    ("WELCOME_TALK", "Welcome Talk"),
    ("NORMAL", "Normal"),
    ("LUNCH", "Lunch"),
)

SPONSOR_PLAN_CHOICES = (
    ("PLATINUM", "Platinum"),
    ("GOLD", "Gold"),
    ("SUPPORTER", "Supporter"),
)


def validate_max_duration(value):
    if value > timedelta(hours=1000):
        raise ValidationError("Maximum duration is 1000 hours.")


def validate_min_duration(value):
    if value < timedelta(seconds=0):
        raise ValidationError("Minimum duration is 0 second.")


class Speaker(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    tag_line = models.CharField(max_length=255, blank=True)
    profile_pic_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    title_en = models.CharField(max_length=255)
    title_ja = models.CharField(max_length=255, blank=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_en


class SessionCategory(models.Model):
    title_en = models.CharField(max_length=255)
    title_ja = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Session categories"

    def __str__(self):
        return self.title_en


class ConferenceSession(models.Model):
    title_en = models.CharField(max_length=255)
    title_ja = models.CharField(max_length=255, blank=True)
    description_en = models.TextField(blank=True)
    description_ja = models.TextField(blank=True)
    target_audience = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    slide_url = models.URLField(blank=True)
    message_en = models.TextField(blank=True)
    message_ja = models.TextField(blank=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(
        validators=[validate_max_duration, validate_min_duration],
        blank=True,
        null=True,
    )
    language = models.CharField(
        max_length=8,
        choices=LANGUAGE_CHOICES,
        default="ENGLISH",
    )
    session_type = models.CharField(
        max_length=12,
        choices=SESSION_TYPE_CHOICES,
        default="NORMAL",
    )
    category = models.ForeignKey(
        SessionCategory,
        on_delete=models.CASCADE,
        related_name="conference_sessions",
        blank=True,
        null=True,
    )
    is_service_session = models.BooleanField(default=False)
    interpretation_target = models.BooleanField(default=False)
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="conference_sessions",
        blank=True,
        null=True,
    )
    speakers = models.ManyToManyField(
        Speaker,
        related_name="conference_sessions",
        blank=True,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="conference_sessions",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_en


class SessionLike(models.Model):
    session = models.ForeignKey(
        ConferenceSession,
        on_delete=models.CASCADE,
        related_name="session_likes",
    )
    device_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.session.title_en} - {self.device_id}"


class Sponsor(models.Model):
    title = models.CharField(max_length=255)
    logo_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    plan = models.CharField(
        max_length=9,
        choices=SPONSOR_PLAN_CHOICES,
        default="SUPPORTER",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


#podcasts here


class Author(models.Model):
    id=models.CharField(primary_key=True,max_length=50)
    name= models.CharField(max_length=100)
    url=models.URLField(default='')
    pic_url=models.URLField(default='')
    class Meta:
        db_table = 'AUTHORS'

class Podcast(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=100)
    description = models.TextField()
    episode_amount = models.IntegerField()
    url=models.URLField(default='')
    tags=models.TextField()
    class Meta:
        db_table = 'PODCASTS'
class Episode(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    audio_url = models.URLField()
    url=models.URLField(default='')
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='episodes')
    class Meta:
        db_table = 'EPISODES'
