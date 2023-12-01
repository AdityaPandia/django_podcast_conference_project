# Generated by Django 4.2.7 on 2023-11-26 11:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conferences', '0005_alter_conferencesession_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='conferencesession',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conference_sessions', to=settings.AUTH_USER_MODEL),
        ),
    ]