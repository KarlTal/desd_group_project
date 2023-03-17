from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

urlpatterns = [
    # Generic URLs.
    path('', views.home, name='ClubRepDashboard'),
]

urlpatterns += staticfiles_urlpatterns()
