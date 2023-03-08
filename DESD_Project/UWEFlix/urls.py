from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

urlpatterns = [
    # Generic URLs.
    path('', views.home, name='Homepage'),
    path('login/', views.login_user, name='Login'),
    path('logout/', views.logout_user, name='Logout'),
    path('register/', views.register, name='Register'),
]

urlpatterns += staticfiles_urlpatterns()
