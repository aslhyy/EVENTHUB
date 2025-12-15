from rest_framework import serializers
from .models import TicketType, Ticket




class TicketTypeSerializer(serializers.ModelSerializer):
    available_quantity = serializers.IntegerField(read_only=True)
    is_available = serializers.BooleanField(read_only=True)


    class Meta:
        model = TicketType
        fields = [
            'id',
            'event',
            'name',
            'price',
            'quantity',
            'sold_count',
            'available_quantity',
            'sale_start',
            'sale_end',
            'is_available'
        ]
        read_only_fields = ['sold_count']


class TicketSerializer(serializers.ModelSerializer):
    is_valid = serializers.BooleanField(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "ticket_type",
            "user",
            "purchase_date",
            "price_paid",
            "status",
            "is_valid",
        ]
        read_only_fields = [
            "id",
            "user",
            "purchase_date",
            "status",
            "price_paid",   # 👈🔥 ESTA ERA LA QUE FALTABA
        ]
