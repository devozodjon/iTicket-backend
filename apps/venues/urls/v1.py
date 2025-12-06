from django.urls import path

from apps.venues.views.venue_create import VenueListCreateApiView
from apps.venues.views.venue_detail import VenueDetailApiView

app_name = "venues"

urlpatterns = [
    path("", VenueListCreateApiView.as_view(), name="venue-list-create"),
    path("<int:pk>/", VenueDetailApiView.as_view(), name="venue-detail"),
]
