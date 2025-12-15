from rest_framework import serializers
from .models import Sponsor, EventSponsor

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = [
            'id',
            'name',
            'logo',
            'website',
            'created_at'
        ]
        read_only_fields = ['created_at']

class EventSponsorSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    duration_days = serializers.IntegerField(read_only=True)


    class Meta:
        model = EventSponsor
        fields = [
            'id',
            'sponsor',
            'event',
            'level',
            'contribution_amount',
            'start_date',
            'end_date',
            'is_active',
            'duration_days',
            'created_at'
        ]
        read_only_fields = ['created_at']