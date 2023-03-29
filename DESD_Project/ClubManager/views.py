from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render

from CinemaManager.views import cinema_dashboard
from UWEFlix.decorators import *
from UWEFlix.forms import *
from .forms import *
from UWEFlix.models import *

# The handler for the homepage of the website.
@login_required(login_url='/login')
@allowed_users(allowed_roles='ClubRepresentative')
def rep_dashboard(request):
    return render(request, 'ClubManager/home.html', {})

@login_required(login_url='login')
@allowed_users(allowed_roles="ClubRepresentative")
def view_all_club_transactions(request):
    club_transactions = Booking.objects.get(user_email=request.user.email) #Gets all the bookings associated with the user's email
    
    context = {
        'club_transactions': club_transactions,
    }
    return render(request, 'ClubManager/view_all_club_transactions.html', {context})

@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def view_clubs(request):
    # Lookup all clubs
    clubs = Club.objects.all()
    return render(request, 'ClubManager/view_clubs.html', {'clubs': clubs})


@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def view_club_reps(request):
    # Lookup all club reps
    club_reps = UserProfile.objects.exclude(club__isnull=True) 
    print("hello")
    print(club_reps)
    return render(request, 'ClubManager/view_reps.html', {'club_reps': club_reps})


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
                  'ClubManager/add_club.html',
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
        return render(request, 'ClubManager/update_club.html', {'club': lookup, 'form': form})

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
        lookup = UserProfile.objects.get(id=rep_id)
        form = CreateClubRepForm(request.POST or None, instance=lookup)

        if form.is_valid():
            form.save()
            return redirect(view_club_reps)
        # Render the page.
        return render(request, 'ClubManager/update_rep.html', {'club_rep': lookup, 'form': form})

    # Redirect back to the homepage.
    print("failed")
    return redirect(cinema_dashboard)


@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def delete_club_rep(request, rep_id):
    if rep_id:
        lookup = UserProfile.objects.get(id=rep_id)
        user_lookup = User.objects.get(id=lookup.user_obj.id)
        # lookup.delete()
        user_lookup.delete()
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
            user.is_active = True #Makes the account active
            club_rep = club_rep_form.save(commit=False)
            club_rep.user_obj = user
            club_rep.save()
            user.username = int(club_rep.id) + 1000
            user = user_form.save()
            group = Group.objects.get(name='ClubRepresentative')
            user.groups.add(group)
            return redirect(view_club_reps)
        else:
            print("Not valid")
    return render(request,
                  'ClubManager/add_rep.html',
                  {'user_form': user_form, 'club_rep_form': club_rep_form})
