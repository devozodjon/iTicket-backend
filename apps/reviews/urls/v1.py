from django.urls import path

from apps.orders.views.order_create import OrderListCreateApiView

app_name = 'orders'

urlpatterns = [
    path('',OrderListCreateApiView.as_view(),name='reviews')
]