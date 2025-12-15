
from django.contrib import admin


# Register your models here.
from .models import Attendee




@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'event',
        'status',
        'check_in_time',
        'created_at'
    ]
    list_filter = ['status', 'event']
    search_fields = ['user__username', 'event__title']
    readonly_fields = ['created_at', 'check_in_time']
