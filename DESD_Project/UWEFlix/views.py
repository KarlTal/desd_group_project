from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from CinemaManager.views import cinema_dashboard
from ClubRep.views import rep_dashboard
from .decorators import *
from .forms import *
from CinemaManager.models import *


# View handling for the UWEFlix homepage.
def home(request):
    films = Film.objects.all()
    return render(request, 'UWEFlix/home.html', {'films': films})


def film(request, film_id):
    # If the film_id exists and the form is valid, update the Film database object with the data from the form.
    if film_id:
        lookup = Film.objects.get(id=film_id)

        # Render the page.
        return render(request, 'UWEFlix/film.html', {'film': lookup})

    # Redirect back to the homepage.
    return redirect(home)


# View handling for user logins.
@unauthenticated_user
def login_user(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            group = request.user.groups.all()[0].name
            if "cinemaManager" in group:
                return redirect(cinema_dashboard)
            elif 'student' in group:
                if request.user.student.pending == 0:
                    logout(request)
                    error = "Your student account is not approved yet!"
                    return render(request, 'UWEFlix/login.html', {'error': error})
                else:
                    return redirect(home)
            else:
                return redirect(home)
        else:
            error = "Invalid email/username or password!"

    return render(request, 'UWEFlix/login.html', {'error': error})


# View handling for club rep logins.
@unauthenticated_user
def login_club_rep(request):
    error = None

    if request.method == 'POST':
        club_rep_number = request.POST.get('clubRepNumber')
        password = request.POST.get('password')

        user = authenticate(request, username=club_rep_number, password=password)
        if user is not None:
            login(request, user)
            return redirect(rep_dashboard)
        else:
            error = "Invalid club rep number or password!"

    return render(request, 'UWEFlix/login_club_rep.html', {'error': error})


# View handling for user logging out.
@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    return redirect(login_user)


# View handling for registering a new user.
@unauthenticated_user
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(login_user)

    return render(request, 'UWEFlix/register.html', {'form': form})
