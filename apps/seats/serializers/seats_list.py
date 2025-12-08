from rest_framework import serializers
from apps.seats.models import Seat
from apps.seats.serializers.section_list import SeatSectionDetailSerializer


class SeatCreateSerializer(serializers.ModelSerializer):
    section_id = serializers.PrimaryKeyRelatedField(
        queryset=SeatSectionDetailSerializer.Meta.model.objects.all(),
        source='section',
        write_only=True,
        required=False,
        allow_null=True
    )
    event_id = serializers.PrimaryKeyRelatedField(
        queryset=Seat._meta.get_field('event').related_model.objects.all(),
        source='event',
        write_only=True
    )

    class Meta:
        model = Seat
        fields = ['event_id', 'section_id', 'row', 'number', 'price', 'is_reserved']


class SeatDetailSerializer(serializers.ModelSerializer):
    section = SeatSectionDetailSerializer(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(read_only=True, source='event.id')

    class Meta:
        model = Seat
        fields = ['id', 'event_id', 'section', 'row', 'number', 'price', 'is_reserved', 'created_at']
