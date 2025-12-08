from rest_framework import serializers

from apps.orders.models import Order
from apps.orders.serialziers.order_create import TicketSerializer


class OrderDetailSerializer(serializers.ModelSerializer):
    seats = serializers.StringRelatedField(many=True)
    tickets = TicketSerializer(many=True, read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'event', 'event_title', 'seats', 'tickets', 'total_price', 'is_paid', 'created_at']
