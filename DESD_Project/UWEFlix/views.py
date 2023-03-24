from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .decorators import *
from .forms import *


# View handling for the UWEFlix homepage.
def home(request):
    return render(request, 'UWEFlix/home.html', {})


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
            form.save()
            return redirect(login_user)

    return render(request, 'UWEFlix/register.html', {'form': form})
