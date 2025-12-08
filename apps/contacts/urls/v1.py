from django.urls import path

from apps.contacts.views.contact_create import ContactListCreateApiView
from apps.contacts.views.contact_detail import ContactDetailApiView, ContactListApiView

app_name = 'contacts'

urlpatterns = [
    path('',ContactListCreateApiView.as_view(),name='contact-list'),
    path('get-all/',ContactListApiView.as_view(),name='contact-list'),
    path('<int:pk>/',ContactDetailApiView.as_view(),name='contact-detail'),
]
