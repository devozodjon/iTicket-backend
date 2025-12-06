from rest_framework import serializers

from apps.events.models import Category
from apps.shared.mixins.translation_mixins import TranslatedFieldsWriteMixin


class CategoryTranslationMixin:
    """Shared configuration for OnBoarding serializers"""
    translatable_fields = ['name', 'description']
    media_fields = ['image']


class CategoryCreateSerializer(TranslatedFieldsWriteMixin, serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name', 'description'
        ]
