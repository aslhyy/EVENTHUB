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
# en este archivo se registran los modelos Sponsor y EventSponsor en el admin de Django