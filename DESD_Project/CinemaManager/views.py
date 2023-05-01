import math
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from UWEFlix.decorators import allowed_users
from .forms import *


# The handler for the homepage of the website.
@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def cinema_dashboard(request):
    # Lookup all current films, screens and showings, so we can display them on the page.
    films = Film.objects.all()
    screens = Screen.objects.all()
    showings = Showing.objects.all()

    # Render the page.
    return render(request, 'CinemaManager/home.html', {'films': films, 'screens': screens, 'showings': showings})


# The handler for the adding film page.
@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def add_film(request):
    # If request is POST and the form used on the page is valid, save it to the database.
    if request.POST:
        form = FilmForm(request.POST, request.FILES)  # Added for images
        if form.is_valid():
            form.save()
        return redirect(cinema_dashboard)

    # Render the page.
    return render(request, 'CinemaManager/add_film.html', {'form': FilmForm})


# The handler for the film information updating page.
@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def update_film(request, film_id):
    # If the film_id exists and the form is valid, update the Film database object with the data from the form.
    if film_id:
        lookup = Film.objects.get(id=film_id)
        form = FilmForm(request.POST or None, request.FILES or None, instance=lookup)

        if form.is_valid():
            form.save()
            return redirect(cinema_dashboard)

        # Render the page.
        return render(request, 'CinemaManager/update_film.html', {'film': lookup, 'form': form})

    # Redirect back to the homepage.
    return redirect(cinema_dashboard)


# The handler for deleting a film.
@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
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
    return redirect(cinema_dashboard)


# The handler for adding a new screen page.
@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def add_screen(request):
    if request.POST:
        form = ScreenForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(cinema_dashboard)

    # Render the page.
    return render(request, 'CinemaManager/add_screen.html', {'form': ScreenForm})


# The handler for deleting a screen.
@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def delete_screen(request, screen_id):
    # If a screen_id is provided, lookup the Screen object and delete it.
    if screen_id:
        lookup = Screen.objects.get(screen_id=screen_id)
        lookup.delete()

    # Redirect back to the homepage.
    return redirect(cinema_dashboard)


# The handler for adding a showing page.
@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def add_showing(request):
    if request.POST:
        form = ShowingForm(request.POST)

        if form.is_valid():
            showing = form.save()

            bulk_add = request.POST.get('bulk-add')
            if bulk_add:
                original_time = showing.time

                for i in range(6):
                    original_time = original_time + timedelta(minutes=(math.ceil(showing.film.duration / 30) * 30))
                    Showing.objects.create(film=showing.film, screen=showing.screen, time=original_time, seats_taken=0)

        return redirect(cinema_dashboard)

    # Render the page.
    return render(request, 'CinemaManager/add_showing.html', {'form': ShowingForm})


# The handler for the showing information updating page.
@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def update_showing(request, showing_id):
    # If the showing_id exists and the form is valid, update the Showing database object with the data from the form.
    if showing_id:
        lookup = Showing.objects.get(id=showing_id)
        if lookup:
            form = ShowingForm(request.POST or None, instance=lookup)
            if form.is_valid():
                form.save()
                return redirect(cinema_dashboard)

            # Render the page.
            return render(request, 'CinemaManager/update_showing.html', {'showing': lookup, 'form': form})

    # Redirect back to the homepage.
    return redirect(cinema_dashboard)


# The handler for deleting a showing.
@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def delete_showing(request, showing_id):
    # If a showing_id is provided, lookup the Showing object and delete it.
    if showing_id:
        lookup = Showing.objects.get(id=showing_id)
        lookup.delete()
    # Redirect back to the homepage.
    return redirect(cinema_dashboard)


# View students
@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def approvals(request):
    students = User.objects.filter(groups__name='Student').filter(is_active=False)
    bookings = Booking.objects.filter(pending_cancel=True)
    discounts = UserProfile.objects.exclude(applied_discount=0)
    return render(request, 'CinemaManager/approvals.html',
                  {'students': students, 'bookings': bookings, 'discounts': discounts})


# Approve student discounts
@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def approve_discount(request, user_id, outcome):
    user = User.objects.get(id=user_id)
    profile = UserProfile.objects.get(user_obj=user)

    if outcome == '1':
        profile.discount = profile.applied_discount

    profile.applied_discount = 0
    profile.save()

    return redirect(approvals)


# Approve booking cancellations
@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def approve_booking(request, booking_id):
    booking = Booking.objects.filter(id=booking_id)

    # Reduce the number of seats taken.
    showing = booking.showing
    showing.seats_taken = showing.seats_taken - booking.ticket_count
    showing.save()

    # Delete the booking.
    booking.delete()

    return redirect(approvals)


# Approve student accounts
@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def approve_student(request, student_id):
    student = User.objects.get(id=student_id)

    # Set the student account to active. This is false by default and prevents the
    # user from being able to log in.
    student.is_active = True
    student.save()

    return redirect(approvals)
