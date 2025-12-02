from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.events.models import Category
from apps.events.serializers.category import CategoryCreateSerializer, CategoryDetail
from apps.shared.permissions.is_organizer import IsAdminOrReadOnly
from apps.shared.utils.custom_response import CustomResponse


class CategoryListCreateApiView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            category = serializer.save()
            response_serializer = CategoryDetail(category, context={'request': request})
            return CustomResponse.success(
                message_key="CATEGORY_CREATED",
                data=response_serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        return CustomResponse.error(
            message_key="VALIDATION_ERROR",
            errors=serializer.errors
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('name')
        serializer = CategoryDetail(queryset, many=True, context={'request': request})
        return CustomResponse.success(
            message_key="CATEGORY_LIST",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
            request=request
        )


class CategoryDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetail
    permission_classes = [IsAdminOrReadOnly]  # permission qo‘shildi

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.success(
            message_key="CATEGORY_DETAIL",
            data=serializer.data
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            category = serializer.save()
            return CustomResponse.success(
                message_key="CATEGORY_UPDATED",
                data=self.get_serializer(category).data,
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
            message_key="CATEGORY_DELETED",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT
        )
