from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.seats.models import SeatSection
from apps.seats.serializers.section_list import SeatSectionDetailSerializer


class SeatSectionDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = SeatSection.objects.all()
    serializer_class = SeatSectionDetailSerializer
    permission_classes = [IsAuthenticated]
