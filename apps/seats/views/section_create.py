from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.seats.models import SeatSection
from apps.seats.serializers.section_list import SeatSectionCreateSerializer
from apps.shared.utils.custom_response import CustomResponse


class SeatSectionListCreateApiView(ListCreateAPIView):
    queryset = SeatSection.objects.all().order_by('id')
    serializer_class = SeatSectionCreateSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            section = serializer.save()
            return CustomResponse.success(
                message_key="CREATED_SUCCESSFULLY",
                data=self.get_serializer(section).data,
                status_code=status.HTTP_201_CREATED
            )
        return CustomResponse.error(
            message_key="VALIDATION_ERROR",
            errors=serializer.errors
        )

