from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied

from apps.events.models import Events
from apps.events.serializers.event_detail_serializer import EventDetailSerializer
from apps.shared.utils.custom_response import CustomResponse


class EventDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Events.objects.all()
    serializer_class = EventDetailSerializer
    permission_classes = [AllowAny]  # retrieve uchun

    def retrieve(self, request, *args, **kwargs):
        """Har bir user event detailini ko‘ra oladi"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data
        )

    def update(self, request, *args, **kwargs):
        """Faqat event organizer update qilishi mumkin"""
        instance = self.get_object()

        # Foydalanuvchi organizer emas yoki o'z eventi emas → xatolik
        if not hasattr(request.user, "organizer") or instance.organizer != request.user.organizer:
            raise PermissionDenied("You do not have permission to update this event.")

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            event = serializer.save()
            return CustomResponse.success(
                message_key="UPDATED_SUCCESSFULLY",
                data=self.get_serializer(event).data,
                status_code=status.HTTP_200_OK
            )

        return CustomResponse.error(
            message_key="VALIDATION_ERROR",
            errors=serializer.errors
        )

    def destroy(self, request, *args, **kwargs):
        """Faqat event organizer o‘chirishi mumkin"""
        instance = self.get_object()

        if not hasattr(request.user, "organizer") or instance.organizer != request.user.organizer:
            raise PermissionDenied("You do not have permission to delete this event.")

        instance.delete()
        return CustomResponse.success(
            message_key="DELETED_SUCCESSFULLY",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT
        )
