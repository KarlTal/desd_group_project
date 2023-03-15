from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

urlpatterns = [
    # Generic URLs.
    path('home', views.cinemaManagerHome, name='Homepage'),

]

urlpatterns += staticfiles_urlpatterns()
