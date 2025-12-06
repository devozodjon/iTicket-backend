from rest_framework import serializers

from apps.shared.mixins.translation_mixins import TranslatedFieldsWriteMixin
from apps.users.models.organizer import Organizer
from apps.users.models.user import User


class OrganizerTranslationMixin:
    """Shared configuration for OnBoarding serializers"""
    translatable_fields = ['bio']
    media_fields = ['image']


class OrganizerCreateSerializer(TranslatedFieldsWriteMixin, serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Organizer
        fields = [
            'user',
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
        fields = '__all__'
