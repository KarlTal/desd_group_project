from django.urls import path
from cinemaBookingSystem import views


# URL Conf 

filmsList = views.ListOfFilms.as_view(
    context_object_name = "list_of_films",
    template_name = "cinemaBookingSystem/HomePage.html",
)

urlpatterns = [
    path("hello2/", views.helloWorld),
    path("", filmsList, name = "homePage"),
    path("registration/", views.RegistrationPage, name = "registrationPage"),
    path("userdetails/", views.getUserData, name="userDetailsPage"),
    path("userdetails/update/<int:id>", views.updateUser, name="userDetails"),
    path("userdetails/delete/<int:id>", views.deleteUser, name="delete"),

]