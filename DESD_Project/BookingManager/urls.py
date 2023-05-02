from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

urlpatterns = [
    # Club related URLs.
    path('', views.home, name='Booking Redirect'),
    path('book_film/<film_id>:<showing_id>', views.book_film, name='Book Film'),
    path('payment/<unique_key>', views.payment, name='Payment'),
    path('confirmation/<booking_id>:<unique_key>', views.confirmation, name='Booking Confirmed'),
    path('cancel_booking/<booking_id>', views.cancel_booking, name='Cancel Booking'),
]

urlpatterns += staticfiles_urlpatterns()
