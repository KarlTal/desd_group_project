from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

urlpatterns = [
    # Generic URLs.
    path('', views.home, name='AccountManagerDashboard'),

]

urlpatterns += staticfiles_urlpatterns()
