from rest_framework import status
from rest_framework.generics import ListCreateAPIView

from apps.events.models import Events
from apps.events.serializers.event_create_serializer import EventCreateSerializer, EventListSerializer
from apps.events.serializers.event_detail_serializer import EventDetailSerializer
from apps.shared.permissions.mobile import IsMobileOrWebUser
from apps.shared.utils.custom_pagination import CustomPageNumberPagination
from apps.shared.utils.custom_response import CustomResponse


class EventListCreateApiView(ListCreateAPIView):
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsMobileOrWebUser]

    def get_queryset(self):
        return Events.objects.filter(is_active=True).order_by("-id")

    def get_serializer_class(self):
        request = self.request

        # POST → faqat create serializer
        if request.method == "POST":
            return EventCreateSerializer

        # GET + WEB → list serializer
        if request.method == "GET" and getattr(request, "device_type", None) == "WEB":
            return EventListSerializer

        # Mobile → detail serializer
        return EventDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            obj = serializer.save()

            response_data = EventDetailSerializer(
                obj,
                context={'request': request}
            ).data

            return CustomResponse.success(
                message_key="SUCCESS_MESSAGE",
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
