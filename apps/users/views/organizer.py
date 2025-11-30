from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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
                message_key="ORGANIZER_CREATED",
                data=response_serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        return CustomResponse.error(
            message_key="VALIDATION_ERROR",
            errors=serializer.errors
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('company_name')
        serializer = OrganizerDetailSerializer(queryset, many=True, context={'request': request})
        return CustomResponse.success(
            message_key="ORGANIZER_LIST",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
            request=request
        )


class OrganizerDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.success(
            message_key="ORGANIZER_DETAIL",
            data=serializer.data
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            organizer = serializer.save()
            return CustomResponse.success(
                message_key="ORGANIZER_UPDATED",
                data=self.get_serializer(organizer).data,
                status_code=status.HTTP_200_OK
            )
        return CustomResponse.error(
            message_key="VALIDATION_ERROR",
            errors=serializer.errors
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return CustomResponse.success(
            message_key="ORGANIZER_DELETED",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT
        )
