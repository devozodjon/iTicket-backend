from django.urls import path, include

urlpatterns = [
    path('users/', include(('apps.users.urls.v1', 'users'), namespace='users')),
    path('events/', include(('apps.events.urls.v1', 'events'), namespace='events')),
    path('orders/', include(('apps.orders.urls.v1', 'orders'), namespace='orders')),
    path('reviews/', include(('apps.reviews.urls.v1', 'reviews'), namespace='reviews')),
    path('seats/', include(('apps.seats.urls.v1', 'seats'), namespace='seats')),
    path('venues/', include(('apps.venues.urls.v1', 'venues'), namespace='venues')),
    path('contacts/', include(('apps.contacts.urls.v1', 'contacts'), namespace='contacts')),
]
