from django.urls import path

from apps.events.views.category import CategoryListCreateApiView, CategoryDetailApiView
from apps.events.views.event_detail import EventDetailApiView
from apps.events.views.event_list import EventListCreateApiView

app_name = 'events'

urlpatterns = [
    path('categories/', CategoryListCreateApiView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailApiView.as_view(), name='category-detail'),

    path('', EventListCreateApiView.as_view(), name='event-list-create'),
    path('<int:pk>/', EventDetailApiView.as_view(), name='event-detail'),
]
