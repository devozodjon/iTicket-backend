from django.urls import path

from apps.orders.views import home

app_name = 'orders'

urlpatterns = [
    path('',home)
]