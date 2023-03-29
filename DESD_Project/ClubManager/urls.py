from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

urlpatterns = [
    # Generic URLs.
    path('', views.rep_dashboard, name='ClubRepDashboard'),
    path('view_all_club_transactions',views.view_all_club_transactions, name="View Club Transactions"),

    # Club related URLs.
    path('view_clubs/', views.view_clubs, name="View Clubs"),
    path('add_club/', views.add_club, name="Add Club"),
    path('update_club/<club_id>', views.update_club, name='Update Club'),
    path('delete_club/<club_id>', views.delete_club, name='Delete Club'),

    # Club representative related URLs.
    path('view_reps/', views.view_club_reps, name="View Reps"),
    path('add_rep/', views.register_club_rep, name="Add Club Rep"),
    path('update_rep/<rep_id>', views.update_club_rep, name='Update Club Rep'),
    path('delete_rep/<rep_id>', views.delete_club_rep, name='Delete Club Rep'),
]

urlpatterns += staticfiles_urlpatterns()

