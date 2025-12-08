from rest_framework import serializers
from apps.seats.models import SeatSection
from apps.venues.serializers import VenueListSerializer


class SeatSectionCreateSerializer(serializers.ModelSerializer):
    venue_id = serializers.PrimaryKeyRelatedField(
        queryset=VenueListSerializer.Meta.model.objects.all(),
        source='venue',
        write_only=True
    )

    class Meta:
        model = SeatSection
        fields = ['name', 'description', 'venue_id']


class SeatSectionDetailSerializer(serializers.ModelSerializer):
    venue = VenueListSerializer(read_only=True)

    class Meta:
        model = SeatSection
        fields = ['id', 'name', 'description', 'venue', 'created_at']
