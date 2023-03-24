from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

urlpatterns = [
    # Generic URLs.
    path('', views.home, name='Homepage'),
    path('login/', views.login_user, name='Login'),
    path('login/clubRep', views.login_club_rep, name='ClubRepLogin'),
    path('logout/', views.logout_user, name='Logout'),
    path('register/', views.register, name='Register'),
    path('register/student', views.registerStudent, name='RegisterStudent'),

]

urlpatterns += staticfiles_urlpatterns()
