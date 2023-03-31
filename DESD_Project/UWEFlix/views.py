from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from CinemaManager.views import cinema_dashboard
from ClubManager.views import rep_dashboard
from UWEFlix.models import *
from .decorators import *
from .forms import *


# View handling for the UWEFlix homepage.
def home(request):
    films = Film.objects.all()
    return render(request, 'UWEFlix/home.html', {'films': films})


# View handling for viewing available Films at UWEFlix.
def film(request, film_id):
    # If the film_id exists and the form is valid, update the Film database object with the data from the form.
    if film_id:
        lookup = Film.objects.get(id=film_id)
        showings = Showing.objects.filter(film=lookup)

        # Render the page.
        return render(request, 'UWEFlix/film.html', {'film': lookup, 'showings': showings})

    # Redirect back to the homepage.
    return redirect(home)


# View handling for user profile.
@login_required(login_url='/login')
def profile(request):
    user_profile = UserProfile.objects.get(user_obj=request.user)
    lookup = Booking.objects.filter(user_email=request.user.email)
    return render(request, 'UWEFlix/profile.html', {'profile': user_profile, 'bookings': lookup})


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

            if "CinemaManager" in group:
                return redirect(cinema_dashboard)
            elif 'Student' in group:
                if not request.user.is_active:
                    logout(request)
                    error = "Your student account has not yet been approved!"
                else:
                    return redirect(home)
            elif 'ClubRepresentative' in group:
                return redirect(rep_dashboard)
            else:
                return redirect(home)
        else:
            error = "Invalid email/username or password!"

    return render(request, 'UWEFlix/login.html', {'error': error})


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
            set_user_group(form.save(), 'Student')
            return redirect(login_user)

    return render(request, 'UWEFlix/register.html', {'form': form})

def about(request):
    return render(request, 'UWEFlix/about.html')

def slideshow(request):
    return render(request, 'UWEFlix/slideshow.html')
