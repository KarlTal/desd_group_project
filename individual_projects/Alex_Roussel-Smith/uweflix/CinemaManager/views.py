from django.shortcuts import render, redirect

from .forms import *
from .models import *


# The handler for the homepage of the website.
def home(request):
    # Lookup all current films, screens and showings, so we can display them on the page.
    films = Film.objects.all()
    screens = Screen.objects.all()
    showings = Showing.objects.all()

    # Render the page.
    return render(request, 'CinemaManager/home.html', {'films': films, 'screens': screens, 'showings': showings})


# The handler for the adding film page.
def add_film(request):
    # If request is POST and the form used on the page is valid, save it to the database.
    if request.POST:
        form = FilmForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(home)

    # Render the page.
    return render(request, 'CinemaManager/add_film.html', {'form': FilmForm})


# The handler for the film information updating page.
def update_film(request, film_id):
    # If the film_id exists and the form is valid, update the Film database object with the data from the form.
    if film_id:
        lookup = Film.objects.get(id=film_id)
        form = FilmForm(request.POST or None, instance=lookup)

        if form.is_valid():
            form.save()
            return redirect(home)

        # Render the page.
        return render(request, 'CinemaManager/update_film.html', {'film': lookup, 'form': form})

    # Redirect back to the homepage.
    return redirect(home)


# The handler for deleting a film.
def delete_film(request, film_id):
    # If a film_id exists, lookup the film and also any showings that contain that film. If there exists a showing
    # that is displaying that film, send an error message to the user. Otherwise, delete the Film.
    if film_id:
        lookup = Film.objects.get(id=film_id)
        showing = Showing.objects.filter(film=lookup)

        if showing:
            form = FilmForm(request.POST or None, instance=lookup)
            error_msg = "You cannot delete a Film that has a Showing!"
            return render(request, 'CinemaManager/update_film.html', {'film': lookup, 'form': form, 'error': error_msg})

        lookup.delete()

    # Redirect back to the homepage.
    return redirect(home)


# The handler for adding a new screen page.
def add_screen(request):
    if request.POST:
        form = ScreenForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(home)

    # Render the page.
    return render(request, 'CinemaManager/add_screen.html', {'form': ScreenForm})


# The handler for deleting a screen.
def delete_screen(request, screen_id):
    # If a screen_id is provided, lookup the Screen object and delete it.
    if screen_id:
        lookup = Screen.objects.get(screen_id=screen_id)
        lookup.delete()

    # Redirect back to the homepage.
    return redirect(home)


# The handler for adding a showing page.
def add_showing(request):
    if request.POST:
        form = ShowingForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(home)

    # Render the page.
    return render(request, 'CinemaManager/add_showing.html', {'form': ShowingForm})


# The handler for the showing information updating page.
def update_showing(request, showing_id):
    # If the showing_id exists and the form is valid, update the Showing database object with the data from the form.
    if showing_id:
        lookup = Showing.objects.get(id=showing_id)
        if lookup:
            form = ShowingForm(request.POST or None, instance=lookup)
            if form.is_valid():
                form.save()
                return redirect(home)

            # Render the page.
            return render(request, 'CinemaManager/update_showing.html', {'showing': lookup, 'form': form})

    # Redirect back to the homepage.
    return redirect(home)


# The handler for deleting a showing.
def delete_showing(request, showing_id):
    # If a showing_id is provided, lookup the Showing object and delete it.
    if showing_id:
        lookup = Showing.objects.get(id=showing_id)
        lookup.delete()

    # Redirect back to the homepage.
    return redirect(home)
