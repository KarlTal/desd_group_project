from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

urlpatterns = [
    # Generic URLs.
    path('', views.cinema_dashboard, name='Dashboard'),

    # Film related URLs.
    path('add_film/', views.add_film, name='Add New Film'),
    path('update_film/<film_id>', views.update_film, name='Update Film'),
    path('delete_film/<film_id>', views.delete_film, name='Delete Film'),

    # Screen related URLs.
    path('add_screen/', views.add_screen, name='Add Screen'),
    path('delete_screen/<screen_id>', views.delete_screen, name='Delete Screen'),

    # Showings related URLs.
    path('add_showing/', views.add_showing, name='Add Showing'),
    path('update_showing/<showing_id>', views.update_showing, name='Update Showing'),
    path('delete_showing/<showing_id>', views.delete_showing, name='Delete Showing'),

    # Approval of accounts
    path('approvals/', views.approvals, name="View Approvals"),
    path('approve_booking/<booking_id>', views.approve_booking, name='Approve Booking'),
    path('approve_student/<student_id>', views.approve_student, name='Approve Student'),
    path('approve_discount/<user_id>:<outcome>', views.approve_discount, name='Approve Discount'),
    path('approve_rep/<student_id>:<outcome>', views.approve_rep, name="Approve Club Rep Application")

]

urlpatterns += staticfiles_urlpatterns()
