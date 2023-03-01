from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import UserDetails
from django.shortcuts import redirect
from django.views.generic import ListView
from cinemaBookingSystem.models import FilmDetails
from cinemaBookingSystem.models import UserDetails
from django.urls import reverse
from cinemaBookingSystem.forms import UpdateForm

# This is the file in which the backend functionality of each webpage must be written

def RegistrationPage(request):
    if request.method == "POST":
        if request.POST.get("first_name_form") and request.POST.get("last_name_form") and request.POST.get("date_of_birth_form") and request.POST.get("email_form") and request.POST.get("address_form") and request.POST.get("username_form") and request.POST.get("password_form"):
            user_details = UserDetails()
            user_details.first_name = request.POST.get("first_name_form")
            user_details.last_name = request.POST.get("last_name_form")
            user_details.date_of_birth = request.POST.get("date_of_birth_form")
            user_details.email = request.POST.get("email_form")
            user_details.address = request.POST.get("address_form")
            user_details.username = request.POST.get("username_form")
            user_details.password = request.POST.get("password_form")
            user_details.save()
        return redirect("homePage")
    else:
        return render(request, "cinemaBookingSystem/Registration.html")

def getUserData(request):
    userSpecificData = UserDetails.objects.filter(first_name="Adrian").values()
    print(userSpecificData)
    userDetailsPage = loader.get_template("cinemaBookingSystem/UserDetails.html")
    context = {
        "firstUser": userSpecificData
    }
    return HttpResponse(userDetailsPage.render(context, request))

def updateUser(request, id):
    individualUser = UserDetails.objects.get(id=id)
    form = UpdateForm(instance = individualUser)

    if request.method == "POST":
        form = UpdateForm(request.POST or None, instance=individualUser)
        if form.is_valid():
            form.save()
            return redirect("homePage")
    else:
        return render(request, "cinemaBookingSystem/UpdateUserDetails.html", {"form": form})

def deleteUser(request, id):
    user = UserDetails.objects.get(id=id)
    user.delete()
    return redirect("homePage")

def helloWorld(request):
    return render(request, "hello2.html")

class homePage(ListView):
    model = FilmDetails
    #return render(request, "cinemaBookingSystem/HomePage.html")

def UserDetailsPage(request):
    return render(request, "cinemaBookingSystem/UserDetails.html")

class ListOfFilms(ListView):
    model = FilmDetails




