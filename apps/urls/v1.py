from django.urls import path, include

urlpatterns = [
    path('users/', include('apps.users.urls.v1', namespace='users')),
    path('events/', include('apps.events.urls.v1', namespace='events')),
]
