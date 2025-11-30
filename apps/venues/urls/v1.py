from django.urls import path

from apps.events.views import home

urlpatterns = [
    path('',home)
]