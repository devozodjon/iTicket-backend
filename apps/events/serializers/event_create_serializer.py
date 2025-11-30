from rest_framework import serializers

from apps.events.models import Events
from apps.shared.mixins.translation_mixins import (
    TranslatedFieldsWriteMixin,
)


class EventTranslationMixin:
    """Shared configuration for OnBoarding serializers"""
    translatable_fields = ['title', 'description']
    media_fields = ['image']


class EventCreateSerializer(TranslatedFieldsWriteMixin, serializers.ModelSerializer):
    real_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Events
        fields = [
            'title', 'description', 'ticket_price', 'real_price',
            'category', 'organizer', 'venue',
            'start_datetime', 'end_datetime', 'status',
        ]

    @staticmethod
    def get_real_price(self, obj):
        if hasattr(obj, 'discount') and obj.discount:
            return obj.ticket_price - (obj.ticket_price * obj.discount / 100)
        return obj.ticket_price


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        exclude = ['title', 'description']

