import re
from django.utils.timezone import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView
from django.template import loader
from django.urls import reverse
#----------------------------------------------------------------Models-------------------------------------------------------------------------------
from UWEFlix.models import Accounts, Clubs, ClubReps, Films
#----------------------------------------------------------------Forms-------------------------------------------------------------------------------
from UWEFlix.forms import RegisterFilmForm,RegisterAccountForm,UpdateFilmForm,UpdateAccountForm
#----------------------------------------------------------------Classes-------------------------------------------------------------------------------
class Film():

    def addFilm(request):
        """Create a film"""
        form = RegisterFilmForm()
        if request.method == "POST":
            form = RegisterFilmForm(request.POST or None, request.FILES)
            if form.is_valid():
                form.save(commit=True)
                return redirect("films")
        else:
            return render(request, "UWEFlix/addFilm.html", {"form": form})
    
    def deleteFilm(request,id):
        """Delete a film"""
        film = Films.objects.get(id=id)
        film.delete()
        return redirect("films")


    def updateFilm(request,id):
        """Update a film"""
        film = Films.objects.get(id=id)
        form = UpdateFilmForm(instance=film)

        if request.method == 'POST':
            form = UpdateFilmForm(request.POST or None,request.FILES or None,instance=film)
            if form.is_valid():
                form.save()
                return redirect("films")
        else:
            return render(request, "UWEFlix/updateFilms.html",{"form": form})

class Account():

    def addAccount(request,):
        """Create an account"""
        form = RegisterAccountForm()
        if request.method == "POST":
            form = RegisterAccountForm(request.POST or None,)
            if form.is_valid():
                form.save(commit=True)
                return redirect("home")
        else:
            return render(request, "UWEFlix/addAccount.html", {"form": form})

    def deleteAccount(request,id):
        """Delete a specific account"""
        account = Accounts.objects.get(id=id)
        account.delete()
        return redirect("home")

    def updateAccount(request,id):
        """Update a specific account"""
        account = Accounts.objects.get(id=id)
        form = UpdateAccountForm(instance=account)

        if request.method == 'POST':
            form = UpdateAccountForm(request.POST or None,instance=account)
            if form.is_valid():
                form.save()
                return redirect("home")
        else:
            return render(request, "UWEFlix/updateAccount.html",{"form": form})

#----------------------------------------------------------------Views-------------------------------------------------------------------------------
class HomeListView(ListView):
    """Renders the home page, with a list of all accounts."""
    model = Accounts
    filmObj = Film()
    accountObj = Account()
    
    def get_context_data(self, **kwargs):
        context= super(HomeListView,self).get_context_data(**kwargs)
        return context

class FilmListView(ListView):
    """Renders the view films page, with a list of all films."""
    model = Films
    def get_context_data(self, **kwargs):
        context = super(FilmListView,self).get_context_data(**kwargs)
        return context

class ClubListView(ListView):
    """Renders the view clubs page, with a list of all clubs."""
    model = Clubs
    def get_context_data(self, **kwargs):
        context = super(ClubListView,self).get_context_data(**kwargs)
        return context

class ClubRepListView(ListView):
    """Renders the view club reps page, with a list of all club reps."""
    model = ClubReps
    def get_context_data(self, **kwargs):
        context = super(ClubRepListView,self).get_context_data(**kwargs)
        return context


