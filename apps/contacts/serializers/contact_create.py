from rest_framework import serializers
from apps.contacts.models import Contact
from apps.shared.mixins.translation_mixins import (
    TranslatedFieldsWriteMixin,
)

class ContactTranslationMixin:
    """Shared configuration for OnBoarding serializers"""
    translatable_fields = ['title', 'description']
    media_fields = ['image']


class ContactCreateSerializer(TranslatedFieldsWriteMixin,serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'id','company_name','phone','phone_2',
            'email','support_email','address',
            'work_hours','telegram','instagram',
            'facebook','youtube','terms_url',
            'privacy_policy_url','google_map',
            'created_at','updated_at',
        ]

class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'id', 'company_name', 'phone', 'phone_2',
            'email', 'support_email', 'address',
            'work_hours', 'telegram', 'instagram',
            'facebook', 'youtube', 'terms_url',
            'privacy_policy_url', 'google_map',
        ]