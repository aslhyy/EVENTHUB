from django.contrib import admin
from .models import Sponsor, EventSponsor


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(EventSponsor)
class EventSponsorAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "sponsor")
    list_filter = ("event",)
