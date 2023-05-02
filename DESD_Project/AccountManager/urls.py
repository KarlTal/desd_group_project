from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

urlpatterns = [
    # Generic URLs.
    path('', views.home, name='Account Dashboard'),
    path('update_user/<user_id>', views.update_user, name='Update User'),
    path('delete_user/<user_id>', views.delete_user, name='Delete User'),
    path('view_statement/<email>:<year>:<month>', views.view_statement, name='View Statement'),
    path('download_statement/<email>:<year>:<month>', views.download_statement, name='Download Statement')
]

urlpatterns += staticfiles_urlpatterns()
