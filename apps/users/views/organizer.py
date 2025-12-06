from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView

from apps.users.models.organizer import Organizer
from apps.users.serializers.organizer import OrganizerCreateSerializer, OrganizerDetailSerializer
from apps.shared.utils.custom_response import CustomResponse


class OrganizerListCreateApiView(ListCreateAPIView):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            organizer = serializer.save()
            response_serializer = OrganizerDetailSerializer(organizer, context={'request': request})
            return CustomResponse.success(
                message_key="SUCCESS_MESSAGE",
                data=response_serializer.data,
            )

        return CustomResponse.error(
            message_key="VALIDATION_ERROR",
            errors=serializer.errors
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('company_name')
        serializer = OrganizerDetailSerializer(queryset, many=True, context={'request': request})
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
            request=request
        )


class OrganizerDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = OrganizerDetailSerializer(instance, context={"request": request})
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data
        )

    def destroy(self, request, *args, **kwargs):
        organizer = self.get_object()
        organizer.delete()
        return CustomResponse.success(
            message_key="ORGANIZER_DELETED",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT,
            request=request
        )

