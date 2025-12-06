from rest_framework import status
from rest_framework.generics import ListCreateAPIView

from apps.events.serializers.event_detail_serializer import VenueSerializer
from apps.venues.models import Venue
from apps.shared.permissions.is_organizer import IsOrganizer
from apps.shared.utils.custom_response import CustomResponse


class VenueListCreateApiView(ListCreateAPIView):
    serializer_class = VenueSerializer
    permission_classes = [IsOrganizer]

    def get_queryset(self):
        return Venue.objects.all().order_by("-id")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            venue = serializer.save()
            return CustomResponse.success(
                message_key="CREATED",
                data=self.get_serializer(venue).data,
                status_code=status.HTTP_201_CREATED
            )
        return CustomResponse.validation_error(errors=serializer.errors, request=request)
