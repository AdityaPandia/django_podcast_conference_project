from django.contrib import admin
from .models import *

admin.site.register(Speaker)
admin.site.register(Room)
admin.site.register(SessionCategory)
admin.site.register(ConferenceSession)
admin.site.register(Sponsor)
