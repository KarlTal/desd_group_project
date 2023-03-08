from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import *


# View handling for the UWEFlix homepage.
def home(request):
    return render(request, 'UWEFlix/home.html', {})


# View handling for user logins.
def login_user(request):
    error = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(home)
        else:
            error = "Invalid email or password!"

    return render(request, 'UWEFlix/login.html', {'error': error})


# View handling for user logging out.
def logout_user(request):
    logout(request)
    return redirect(login_user)


# View handling for registering a new user.
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(login_user)

    return render(request, 'UWEFlix/register.html', {'form': form})
