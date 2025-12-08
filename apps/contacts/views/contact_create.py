from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.contacts.models import Contact
from apps.contacts.serializers.contact_create import ContactCreateSerializer, ContactListSerializer

from apps.shared.utils.custom_response import CustomResponse
from apps.shared.utils.custom_pagination import CustomPageNumberPagination


class ContactListCreateApiView(ListCreateAPIView):
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Contact.objects.filter(is_active=True).order_by("-id")

    def get_serializer_class(self):
        request = self.request
        if request.method == "POST":
            return ContactCreateSerializer
        return ContactListSerializer

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            self.perform_create(serializer)

            response_data = ContactListSerializer(
                serializer.instance,
                context={'request': request}
            ).data

            return CustomResponse.success(
                message_key="CREATED",
                data=response_data,
                status_code=status.HTTP_201_CREATED
            )

        return CustomResponse.error(
            message_key="VALIDATION_ERROR",
            errors=serializer.errors
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            page if page is not None else queryset,
            many=True,
            context={'request': request}
        )

        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
            request=request
        )
