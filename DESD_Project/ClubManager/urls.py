from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

urlpatterns = [
    # Generic URLs.
    path('', views.rep_dashboard, name='ClubRepDashboard'),
    path('view_transactions', views.view_transactions, name="View Club Transactions"),

    # Club related URLs.
    path('view_clubs/', views.view_clubs, name="View Clubs"),
    path('add_club/', views.add_club, name="Add Club"),
    path('update_club/<club_id>', views.update_club, name='Update Club'),
    path('delete_club/<club_id>', views.delete_club, name='Delete Club'),

    # Club representative related URLs.
    path('view_reps/', views.view_club_reps, name="View Reps"),
    path('add_rep/<club_id>', views.add_club_rep, name="Add Club Rep"),
    path('update_rep/<rep_id>', views.update_club_rep, name='Update Club Rep'),
    path('delete_rep/<rep_id>', views.delete_club_rep, name='Delete Club Rep'),
    path('settle_transactions_monthly/',views.settle_transactions_monthly, name = "Settle Montly Transactions"),
    path('top_up_credits/<club_rep_id>',views.top_up_credits,name = "Top Up Club Rep Credits"),
]

urlpatterns += staticfiles_urlpatterns()
