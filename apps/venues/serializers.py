from rest_framework import serializers
from apps.venues.models import Venue

class VenueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = [
            'id',
            'name',
            'city',
            'capacity'
        ]


class VenueDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = [
            'id',
            'name',
            'description',
            'address',
            'city',
            'capacity'
        ]
