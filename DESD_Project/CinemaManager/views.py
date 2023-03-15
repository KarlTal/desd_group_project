from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.shortcuts import render, redirect

def cinemaManagerHome(request):
    return render(request, 'CinemaManager/cinemaManagerHome.html', {})
