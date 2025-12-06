from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from apps.shared.permissions.is_organizer import IsOrganizer
from apps.shared.utils.custom_response import CustomResponse
from apps.venues.models import Venue
from apps.venues.serializers import VenueDetailSerializer


class VenueDetailApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = VenueDetailSerializer
    permission_classes = [IsOrganizer]
    lookup_field = "pk"

    def get_queryset(self):
        return Venue.objects.all()

    def retrieve(self, request, *args, **kwargs):
        venue = self.get_object()
        serializer = self.get_serializer(venue)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        venue = self.get_object()
        serializer = self.get_serializer(venue, data=request.data, partial=partial)
        if serializer.is_valid():
            venue = serializer.save()
            return CustomResponse.success(
                message_key="SUCCESS_MESSAGE",
                data=self.get_serializer(venue).data,
                status_code=status.HTTP_200_OK,
                request=request
            )
        return CustomResponse.validation_error(errors=serializer.errors, request=request)

    def destroy(self, request, *args, **kwargs):
        venue = self.get_object()
        venue.delete()
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT,
            request=request
        )
