import math
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from UWEFlix.decorators import allowed_users
from UWEFlix.forms import get_form_errors
from .forms import *


# The handler for the homepage of the website.
@login_required(login_url='/login/')
@allowed_users(allowed_roles='CinemaManager')
def cinema_dashboard(request):
    update_films()

    # Lookup all current films, screens and showings, so we can display them on the page.
    films = Film.objects.all()
    screens = Screen.objects.all()
    showings = Showing.objects.all()
    tickets = TicketType.objects.all()

    # Render the page.
    return render(request, 'CinemaManager/home.html',
                  {'films': films, 'screens': screens, 'showings': showings, 'tickets': tickets})


# =============================================== #
#              FILM API MANAGEMENT                #
# =============================================== #


# The handler for the adding film page.
@login_required(login_url='/login/')
@allowed_users(allowed_roles='CinemaManager')
def add_film(request):
    error_message = ''

    if request.POST:
        form = FilmForm(request.POST)

        # If the form is valid, then make a request to the Film Manager API to add a new Film.
        if form.is_valid():
            # try:
            response = requests.post('http://film-manager:8080/add/',
                                     data={'title': form.cleaned_data.get('title'),
                                           'trailer': form.cleaned_data.get(
                                               'trailer')})

            # Ensure that we receive a valid response, otherwise print the received error.
            if response.status_code != 201:
                error_message = response.text
            else:
                update_films()
                return redirect(cinema_dashboard)
        # except:
        #     error_message = 'Failed to connect to Film backend! Is it down?'
        else:
            error_message = get_form_errors(form)

    # Render the page.
    return render(request, 'CinemaManager/add_film.html', {'error': error_message, 'form': FilmForm})


# The handler for the film information updating page.
@login_required(login_url='/login/')
@allowed_users(allowed_roles='CinemaManager')
def update_film(request, film_id):
    if film_id:
        lookup = Film.objects.get(id=film_id)
        form = UpdateFilmForm(request.POST or None, request.FILES or None, instance=lookup)

        # If the form is valid, then make a request to the Film Manager API to update a Film.
        if form.is_valid():
            try:
                response = requests.post('http://film-manager:8080/update/', data={
                    'id': lookup.id,
                    'title': form.cleaned_data.get('title'),
                    'age_rating': form.cleaned_data.get('age_rating'),
                    'duration': form.cleaned_data.get('duration'),
                    'description': form.cleaned_data.get('description'),
                    'trailer': form.cleaned_data.get('trailer')
                })

                # Ensure that we receive a valid response, otherwise print the received error.
                if response.status_code != 200:
                    error_message = response.json().get('error')
                else:
                    update_films()
                    return redirect(cinema_dashboard)
            except:
                error_message = 'Failed to connect to Film backend! Is it down?'
        else:
            error_message = get_form_errors(form)

        # Render the page.
        return render(request, 'CinemaManager/update_film.html', {'error': error_message, 'film': lookup, 'form': form})

    # Redirect back to the homepage.
    return redirect(cinema_dashboard)


# The handler for deleting a film.
@login_required(login_url='/login/')
@allowed_users(allowed_roles='CinemaManager')
def delete_film(request, film_id):
    # If a film_id exists, lookup the film and also any showings that contain that film. If there exists a showing
    # that is displaying that film, send an error message to the user. Otherwise, delete the Film.
    if film_id:
        lookup = Film.objects.get(id=film_id)
        showing = Showing.objects.filter(film=lookup)
        form = FilmForm(request.POST or None, instance=lookup)

        # If the film has a showing assigned, then display an error message.
        if showing:
            error_message = "You cannot delete a Film that has a Showing!"
        else:
            try:
                # Otherwise, send a request to the Film Manager API to delete the film.
                response = requests.post('http://film-manager:8080/delete/', data={'id': lookup.id})

                # Ensure that we receive a valid response, otherwise print the received error.
                if response.status_code != 200:
                    error_message = response.json().get('error')
                else:
                    update_films()
                    return redirect(cinema_dashboard)
            except:
                error_message = 'Failed to connect to Film backend! Is it down?'

        return render(request, 'CinemaManager/update_film.html', {'film': lookup, 'form': form, 'error': error_message})

    # Redirect back to the homepage.
    return redirect(cinema_dashboard)


# =============================================== #
#       SCREEN, TICKET & SHOWING MANAGEMENT       #
# =============================================== #


# The handler for adding a new screen page.
@login_required(login_url='/login/')
@allowed_users(allowed_roles='CinemaManager')
def add_screen(request):
    error_message = ''

    if request.POST:
        form = ScreenForm(request.POST)

        if form.is_valid():  #
            form.save()
            return redirect(cinema_dashboard)
        else:
            error_message = get_form_errors(form)

    # Render the page.
    return render(request, 'CinemaManager/add_screen.html', {'error': error_message, 'form': ScreenForm})


# The handler for deleting a screen.
@login_required(login_url='/login/')
@allowed_users(allowed_roles='CinemaManager')
def delete_screen(request, screen_id):
    # If a screen_id is provided, lookup the Screen object and delete it.
    if screen_id:
        lookup = Screen.objects.get(screen_id=screen_id)
        lookup.delete()

    # Redirect back to the homepage.
    return redirect(cinema_dashboard)


# The handler for adding a showing page.
@login_required(login_url='/login/')
@allowed_users(allowed_roles='CinemaManager')
def add_showing(request):
    error_message = ''

    if request.POST:
        form = ShowingForm(request.POST)

        if form.is_valid():  #
            showing = form.save()

            bulk_add = request.POST.get('bulk-add')
            if bulk_add:
                original_time = showing.time

                for i in range(6):
                    original_time = original_time + timedelta(minutes=(math.ceil(showing.film.duration / 30) * 30))
                    Showing.objects.create(film=showing.film, screen=showing.screen, time=original_time, seats_taken=0)

            return redirect(cinema_dashboard)
        else:
            error_message = get_form_errors(form)

    # Render the page.
    return render(request, 'CinemaManager/add_showing.html', {'error': error_message, 'form': ShowingForm})


# The handler for the showing information updating page.
@login_required(login_url='/login/')
@allowed_users(allowed_roles='CinemaManager')
def update_showing(request, showing_id):
    # If the showing_id exists and the form is valid, update the Showing database object with the data from the form.
    if showing_id:
        lookup = Showing.objects.get(id=showing_id)

        if lookup:
            form = ShowingForm(request.POST or None, instance=lookup)

            if form.is_valid():  #
                form.save()
                return redirect(cinema_dashboard)
            else:
                error_message = get_form_errors(form)

            # Render the page.
            return render(request, 'CinemaManager/update_showing.html',
                          {'error': error_message, 'showing': lookup, 'form': form})

    # Redirect back to the homepage.
    return redirect(cinema_dashboard)


# The handler for deleting a showing.
@login_required(login_url='/login/')
@allowed_users(allowed_roles='CinemaManager')
def delete_showing(request, showing_id):
    # If a showing_id is provided, lookup the Showing object and delete it.
    if showing_id:
        lookup = Showing.objects.get(id=showing_id)
        lookup.delete()
    # Redirect back to the homepage.
    return redirect(cinema_dashboard)


def update_ticket(request, ticket_id):
    # If the ticket_id exists and the form is valid, update the Ticket database object with the data from the form.
    if ticket_id:
        lookup = TicketType.objects.get(id=ticket_id)

        if lookup:
            form = TicketForm(request.POST or None, instance=lookup)

            if form.is_valid():  #
                form.save()
                return redirect(cinema_dashboard)
            else:
                error_message = get_form_errors(form)

            # Render the page.
            return render(request, 'CinemaManager/update_ticket.html',
                          {'error': error_message, 'ticket': lookup, 'form': form})

    # Redirect back to the homepage.
    return redirect(cinema_dashboard)


# =============================================== #
#                APPROVAL HANDLING                #
# =============================================== #


# View students
@login_required(login_url='/login/')
@allowed_users(allowed_roles='CinemaManager')
def approvals(request):
    students = User.objects.filter(groups__name='Student').filter(is_active=False)
    bookings = Booking.objects.filter(pending_cancel=True)
    discounts = UserProfile.objects.exclude(applied_discount=0)
    rep_apps = UserProfile.objects.exclude(applied_for_rep=0)

    return render(request, 'CinemaManager/approvals.html',
                  {'students': students, 'bookings': bookings, 'discounts': discounts, 'rep_apps': rep_apps})


# Approve student discounts
@login_required(login_url='/login/')
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
@login_required(login_url='/login/')
@allowed_users(allowed_roles='CinemaManager')
def approve_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    showing = Showing.objects.get(booking = booking)
    # Reduce the number of seats taken.
    showing.seats_taken = showing.seats_taken - booking.ticket_count
    showing.save()

    # Delete the booking.
    booking.delete()

    return redirect(approvals)


# Approve student accounts
@login_required(login_url='/login/')
@allowed_users(allowed_roles='CinemaManager')
def approve_student(request, student_id):
    student = User.objects.get(id=student_id)

    # Set the student account to active. This is false by default and prevents the
    # user from being able to log in.
    student.is_active = True
    student.save()

    return redirect(approvals)


# Approve club rep applications
@login_required(login_url='/login/')
@allowed_users(allowed_roles='CinemaManager')
def approve_rep(request, student_id, outcome):
    user = User.objects.get(id=student_id)
    profile = UserProfile.objects.get(user_obj=user)

    if outcome == '1':
        # Set user's group to club rep
        group = Group.objects.get(name="ClubRepresentative")
        current_group = Group.objects.get(name="Student")
        club = Club.objects.get(id=profile.club.id)
        user.groups.add(group)

        # Remove from student group
        user.groups.remove(current_group)

        # Generate club rep id
        profile.applied_for_rep = False
        user.username = int(profile.id) + 1000
        user.save()
        profile.save()

        # Update club has_rep field
        club.has_club_rep = True
        club.save()

        # If they are other applications then deny all of them as there can only be one club rep per club
        users_applying_to_the_same_club = UserProfile.objects.filter(club=profile.club)
        for same_user in users_applying_to_the_same_club:
            if same_user.id == profile.id:
                pass
            else:
                same_user.club = None
                same_user.applied_for_rep = False
                same_user.save()

    else:
        profile.applied_for_rep = False
        profile.club_id = None
        profile.save()

    return redirect(approvals)
