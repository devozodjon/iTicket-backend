from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.seats.models import Seat
from apps.seats.serializers.seats_list import SeatDetailSerializer


class SeatDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatDetailSerializer
    permission_classes = [IsAuthenticated]
