from rest_framework import serializers

from apps.shared.mixins.translation_mixins import TranslatedFieldsWriteMixin
from apps.users.models.organizer import Organizer


class OrganizerTranslationMixin:
    """Shared configuration for OnBoarding serializers"""
    translatable_fields = ['bio']
    media_fields = ['image']


class OrganizerCreateSerializer(TranslatedFieldsWriteMixin, serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = [
            'first_name',
            'last_name',
            'company_name',
            'business_license',
            'bank_account',
            'email',
            'bio',
            'is_active',
        ]


class OrganizerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = [
            'id',
            'first_name',
            'last_name',
            'company_name',
            'business_license',
            'bank_account',
            'email',
            'bio',
            'is_active',
            'user_email',
            'user_full_name',
        ]