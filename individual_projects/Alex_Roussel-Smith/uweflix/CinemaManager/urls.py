from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

urlpatterns = [
    # Generic URLs.
    path('', views.home, name='Homepage'),

    # Film related URLs.
    path('add_film/', views.add_film, name='Add a new Film'),
    path('update_film/<film_id>', views.update_film, name='Update a Films information'),
    path('delete_film/<film_id>', views.delete_film, name='Delete a Film'),

    # Screen related URLs.
    path('add_screen/', views.add_screen, name='Add a Screen'),
    path('delete_screen/<screen_id>', views.delete_screen, name='Delete a Screen'),

    # Showings related URLs.
    path('add_showing/', views.add_showing, name='Add Showing'),
    path('update_showing/<showing_id>', views.update_showing, name='Update a Showing'),
    path('delete_showing/<showing_id>', views.delete_showing, name='Delete a Showing')
]

urlpatterns += staticfiles_urlpatterns()
