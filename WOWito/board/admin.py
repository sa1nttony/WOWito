from django.contrib import admin

from .models import Player, Announcement, Response, New

# Register your models here.
admin.site.register(Player)
admin.site.register(Announcement)
admin.site.register(Response)
admin.site.register(New)