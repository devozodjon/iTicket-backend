from rest_framework import serializers
from apps.events.models import Events
from apps.shared.mixins.translation_mixins import (
    TranslatedFieldsWriteMixin,
)
from django.utils.text import slugify


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
            'category', 'venue',
            'start_datetime', 'end_datetime', 'status',
        ]

    def create(self, validated_data):
        base_slug = slugify(validated_data['title'])
        slug = base_slug
        num = 1
        while Events.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{num}"
            num += 1
        validated_data['slug'] = slug
        return super().create(validated_data)

    @staticmethod
    def get_real_price(obj):
        if hasattr(obj, 'discount') and obj.discount:
            return obj.ticket_price - (obj.ticket_price * obj.discount / 100)
        return obj.ticket_price


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        exclude = ['title', 'description']
