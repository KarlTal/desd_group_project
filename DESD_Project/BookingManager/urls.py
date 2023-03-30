from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

urlpatterns = [
    # Club related URLs.
    path('', views.home, name='Booking Redirect'),
    path('book_film/<film_id>:<showing_id>', views.book_film, name='Book Film'),
]

urlpatterns += staticfiles_urlpatterns()
