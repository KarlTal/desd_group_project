from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_films),
    path('add/', views.add_film),
    path('delete/', views.delete_film),
    path('update/', views.update_film)
]
