from rest_framework import serializers
from apps.orders.models import Order, Ticket
from apps.seats.models import Seat
from apps.shared.mixins.translation_mixins import (
    TranslatedFieldsWriteMixin,
)


class OrderTranslationMixin:
    """Shared configuration for OnBoarding serializers"""
    translatable_fields = ['title', 'description']
    media_fields = ['image']


class TicketSerializer(serializers.ModelSerializer):
    seat_number = serializers.CharField(source='seat.number', read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'seat', 'seat_number', 'issued_at', 'qr_code']


class OrderCreateSerializer(TranslatedFieldsWriteMixin,serializers.ModelSerializer):
    seats = serializers.PrimaryKeyRelatedField(queryset=Seat.objects.filter(is_reserved=False), many=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['event', 'seats', 'total_price']

    @staticmethod
    def validate_seats(value):
        for seat in value:
            if seat.is_reserved:
                raise serializers.ValidationError(f"Seat {seat.number} is already reserved")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        seats = validated_data.pop('seats')
        event = validated_data['event']

        total_price = sum([seat.price for seat in seats])
        order = Order.objects.create(user=user, event=event, total_price=total_price)

        for seat in seats:
            order.seats.add(seat)
            seat.is_reserved = True
            seat.save()

            Ticket.objects.create(order=order, seat=seat)

        event.participants.add(user)

        return order
