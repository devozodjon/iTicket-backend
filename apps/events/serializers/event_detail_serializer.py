from rest_framework import serializers
from apps.events.models import Events, Category
from apps.events.serializers.event_create_serializer import EventTranslationMixin
from apps.shared.mixins.translation_mixins import TranslatedFieldsReadMixin
from apps.venues.models import Venue


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'name', 'description']


class EventDetailSerializer(EventTranslationMixin, TranslatedFieldsReadMixin, serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    venue = VenueSerializer(read_only=True)

    images = serializers.SerializerMethodField()

    class Meta:
        model = Events
        fields = [
            'id',
            'title',
            'description',
            'category',
            'venue',
            'start_datetime',
            'end_datetime',
            'ticket_price',
            'tickets_total',
            'tickets_sold',
            'status',
            'created_at',
            'images'
        ]

    def get_images(self, obj):
        return self._get_media(obj, 'images', 'uz')

