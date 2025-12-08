from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from apps.seats.models import Seat, SeatSection
from apps.seats.serializers import SeatSerializer, SeatSectionSerializer
from apps.shared.utils.custom_response import CustomResponse


# SeatSection CRUD
class SeatSectionListCreateApiView(ListCreateAPIView):
    queryset = SeatSection.objects.all().order_by('id')
    serializer_class = SeatSectionSerializer
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


class SeatSectionDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = SeatSection.objects.all()
    serializer_class = SeatSectionSerializer
    permission_classes = [IsAuthenticated]


# Seat CRUD
class SeatListCreateApiView(ListCreateAPIView):
    queryset = Seat.objects.all().order_by('id')
    serializer_class = SeatSerializer
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
            seat = serializer.save()
            return CustomResponse.success(
                message_key="CREATED_SUCCESSFULLY",
                data=self.get_serializer(seat).data,
                status_code=status.HTTP_201_CREATED
            )
        return CustomResponse.error(
            message_key="VALIDATION_ERROR",
            errors=serializer.errors
        )


class SeatDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [IsAuthenticated]
