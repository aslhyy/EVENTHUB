"""
Serializers para eventos.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Category, Venue, Event

class CategorySerializer(serializers.ModelSerializer):
    events_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon', 'events_count']


class CategoryDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para categorías con eventos."""
    events_count = serializers.IntegerField(read_only=True)
    recent_events = serializers.SerializerMethodField()


    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description', 'icon',
            'events_count', 'recent_events'
        ]


class VenueSerializer(serializers.ModelSerializer):
    full_address = serializers.CharField(read_only=True)

    class Meta:
        model = Venue
        fields = [
            'id', 'name', 'address', 'city', 'state', 'capacity',
            'full_address'
        ]


class EventSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    venue = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = "__all__"

class OrganizerSerializer(serializers.ModelSerializer):
    """Serializer para organizadores."""
    full_name = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'email']


    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


class EventSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    venue = serializers.PrimaryKeyRelatedField(
        queryset=Venue.objects.all()
    )

    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ["organizer", "slug"]

class EventDetailSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    venue = serializers.SerializerMethodField()
    organizer = serializers.SerializerMethodField()
    tickets_sold = serializers.IntegerField(read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)
    is_sold_out = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_past = serializers.BooleanField(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'description',
            'category', 'venue', 'organizer',
            'status', 'capacity',
            'tickets_sold', 'tickets_available',
            'is_free', 'is_online',
            'online_url', 'is_sold_out',
            'is_active', 'is_past'
        ]

    def get_category(self, obj):
        return {
            "id": obj.category.id,
            "name": obj.category.name
        }

    def get_venue(self, obj):
        return {
            "id": obj.venue.id,
            "name": obj.venue.name
        }

    def get_organizer(self, obj):
        return {
            "id": obj.organizer.id,
            "username": obj.organizer.username
        }
    
    def get_tag_list(self, obj):
        return obj.get_tag_list()

class EventStatisticsSerializer(serializers.Serializer):
    """Serializer para estadísticas del evento."""
    total_capacity = serializers.IntegerField()
    tickets_sold = serializers.IntegerField()
    tickets_available = serializers.IntegerField()
    revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    attendees_checked_in = serializers.IntegerField()
    conversion_rate = serializers.FloatField()
