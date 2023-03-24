from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

urlpatterns = [
    # Generic URLs.
    path('', views.rep_dashboard, name='ClubRepDashboard'),
    #Club related URLs.
    path('view_clubs/',views.view_clubs,name="ViewClubs"),
    path('register/club',views.add_club, name="AddClub"),
    path('update_club/<club_id>', views.update_club, name='UpdateClubDetails'),
    path('delete_club/<club_id>', views.delete_club, name='DeleteClub'),


    #Club representative related URLs.
    path('view_club_reps/',views.view_club_reps,name="ViewClubReps"),
    path('register/clubRep',views.register_club_rep, name="AddClubRep"),
    path('update_club_rep/<rep_id>', views.update_club_rep, name='UpdateClubRepDetails'),
    path('delete_club_rep/<rep_id>', views.delete_club_rep, name='DeleteClubRep'),
    # path('book/clubRep/blockBooking',views.block_booking, name="BlockBooking"),
]

urlpatterns += staticfiles_urlpatterns()
