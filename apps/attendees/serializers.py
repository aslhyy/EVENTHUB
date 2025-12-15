from rest_framework import serializers
from .models import Attendee

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = [
            'id',
            'event',
            'user',
            'ticket',
            'status',
            'check_in_time',
            'created_at'
        ]
        read_only_fields = ['user', 'status', 'check_in_time', 'created_at']