from django.contrib import admin


# Register your models here.
from .models import TicketType, Ticket




@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'event',
        'price',
        'quantity',
        'sold_count',
        'available_quantity',
        'sale_start',
        'sale_end'
    ]
    list_filter = ['event']
    search_fields = ['name', 'event__title']
    readonly_fields = ['sold_count']




@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        'ticket_type',
        'user',
        'status',
        'price_paid',
        'purchase_date'
    ]
    list_filter = ['status']
    search_fields = ['user__username', 'ticket_type__name']
    readonly_fields = ['purchase_date']
