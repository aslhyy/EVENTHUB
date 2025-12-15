from django.contrib import admin


# Register your models here.
"""
Configuración del admin para eventos.
"""
from .models import Category, Venue, Event




# =========================
# CATEGORY ADMIN
# =========================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'events_count')
    search_fields = ('name', 'description')




# =========================
# VENUE ADMIN
# =========================
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'capacity')
    list_filter = ('city', 'state')
    search_fields = ('name', 'city', 'address')




# =========================
# EVENT ADMIN
# =========================
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'venue',
        'status',
        'start_date',
        'organizer',
        'tickets_sold',
        'tickets_available'
    )


    list_filter = (
        'status',
        'category',
        'is_free',
        'is_online',
        'start_date',
    )


    search_fields = (
        'title',
        'description',
        'organizer__username',
    )


    prepopulated_fields = {
        'slug': ('title',)
    }


    readonly_fields = (
        'tickets_sold',
        'tickets_available',
    )


    fieldsets = (
        ('Información Básica', {
            'fields': (
                'title',
                'slug',
                'description',
                'category',
                'status',
            )
        }),
        ('Ubicación', {
            'fields': (
                'venue',
                'is_online',
            )
        }),
        ('Fechas del Evento', {
            'fields': (
                'start_date',
                'end_date',
            )
        }),
        ('Configuración', {
            'fields': (
                'capacity',
                'is_free',
                'organizer',
            )
        }),
        ('Estadísticas', {
            'fields': (
                'tickets_sold',
                'tickets_available',
            )
        }),
    )