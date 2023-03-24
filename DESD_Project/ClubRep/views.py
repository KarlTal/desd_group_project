from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render

from CinemaManager.views import cinema_dashboard
from UWEFlix.forms import *
from .decorators import *
from .forms import *


# The handler for the homepage of the website.
@login_required(login_url='/login')
@allowed_users(allowed_roles='ClubRepresentative')
def rep_dashboard(request):
    return render(request, 'ClubRep/home.html', {})


@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def view_clubs(request):
    # Lookup all clubs
    clubs = Club.objects.all()
    return render(request, 'ClubRep/view_clubs.html', {'clubs': clubs})


@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def view_club_reps(request):
    # Lookup all club reps
    club_reps = ClubRepProfile.objects.all()
    return render(request, 'ClubRep/view_club_reps.html', {'club_reps': club_reps})


# View handling for registering a new club representative
@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def add_club(request):
    club_form = CreateClubForm()
    if request.method == 'POST':
        club_form = CreateClubForm(request.POST)
        if club_form.is_valid():
            club_form.save()
            return redirect(view_clubs)
        else:
            print("Not valid")
    return render(request,
                  'ClubRep/create_club.html',
                  {'club_form': club_form})


# The handler for the club information update page
@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def update_club(request, club_id):
    if club_id:
        lookup = Club.objects.get(id=club_id)
        form = CreateClubForm(request.POST or None, instance=lookup)

        if form.is_valid():
            form.save()
            return redirect(view_clubs)

        # Render the page.
        return render(request, 'ClubRep/update_club.html', {'club': lookup, 'form': form})

    # Redirect back to the homepage.
    return redirect(cinema_dashboard)


@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def delete_club(request, club_id):
    if club_id:
        lookup = Club.objects.get(id=club_id)
        lookup.delete()
    # Redirect back to the view clubs.
    return redirect(view_clubs)


# The handler for the club rep information update page
@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def update_club_rep(request, rep_id):
    if rep_id:
        lookup = ClubRepProfile.objects.get(repID=rep_id)
        form = CreateClubRepForm(request.POST or None, instance=lookup)

        if form.is_valid():
            form.save()
            return redirect(view_club_reps)
        # Render the page.
        return render(request, 'ClubRep/update_club_rep.html', {'club_rep': lookup, 'form': form})

    # Redirect back to the homepage.
    print("failed")
    return redirect(cinema_dashboard)


@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def delete_club_rep(request, rep_id):
    if rep_id:
        lookup = ClubRepProfile.objects.get(repID=rep_id)
        lookup.delete()
    # Redirect back to the view clubs.
    return redirect(view_club_reps)


# View handling for registering a new club representative
@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def register_club_rep(request):
    club_rep_form = CreateClubRepForm()
    user_form = CreateUserForm()
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        user_form.username = 'clubRepRandom'
        print(user_form.username)
        club_rep_form = CreateClubRepForm(request.POST)
        if user_form.is_valid() and club_rep_form.is_valid():
            user = user_form.save()
            club_rep = club_rep_form.save(commit=False)
            club_rep.user = user
            club_rep.save()
            user.username = club_rep.repID
            user.email = club_rep.repID
            user = user_form.save()
            group = Group.objects.get(name='clubRep')
            user.groups.add(group)
            return redirect(view_club_reps)
        else:
            print("Not valid")
    return render(request,
                  'ClubRep/register_club_rep.html',
                  {'user_form': user_form, 'club_rep_form': club_rep_form})

# @login_required
# @allowed_users(allowed_roles=['clubRep'])
# def block_booking(request):
#     block_booking_form = MakeBlockBooking()
#     if request.method == 'POST':
#         block_booking_form = MakeBlockBooking(request.POST)
#         if block_booking_form.is_valid():
#             block_booking_form.save()
#             return redirect(cinema_dashboard) #Can change to the tables of clubs
#         else:
#             print("Not valid")
#     return render(request,
#                   'ClubRep/make_block_booking.html',
#                   {'block_booking_form':block_booking_form})
