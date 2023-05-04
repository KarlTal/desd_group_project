from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from CinemaManager.views import cinema_dashboard
from UWEFlix.decorators import *
from UWEFlix.forms import *
from UWEFlix.models import *
from .forms import *


# The handler for the homepage of the website.
@login_required(login_url='/login/')
@allowed_users(allowed_roles='ClubRepresentative')
def rep_dashboard(request):
    error_message = ''
    authenticated = ("successful_club_rep_login" in request.session)

    # Populate the session data with the counter set to 0 to avoid KeyErrors.
    if "successful_club_rep_login" not in request.session:
        request.session["club_rep_login_attempts"] = 0

    if authenticated:
        error_message = ''
        success_message = ''
        user_profile = UserProfile.objects.get(user_obj=request.user)

        to_settle = 0
        all_transactions = Booking.objects.filter(user_email=request.user.email).order_by('date')

        for transaction in all_transactions:
            if not transaction.has_been_paid:
                to_settle = to_settle + transaction.total_price

        if request.method == 'POST':
            if to_settle <= 0:
                error_message = 'You do not have any pending payments!'
            else:
                if user_profile.credits >= to_settle:
                    all_transactions = Booking.objects.filter(user_email=request.user.email).order_by('date')

                    for transaction in all_transactions:
                        if not transaction.has_been_paid:
                            transaction.has_been_paid = True
                            transaction.save()

                    # Register our credit transaction.
                    Transaction.objects.create(user_email=request.user.email, origin='Settling Accounts', type='Debit',
                                               amount=to_settle)

                    user_profile.credits -= to_settle
                    user_profile.save()

                    to_settle = 0

                    success_message = 'All pending payments have been settled!'
                else:
                    error_message = 'You do not have sufficient credits to settle the pending payments!'

        return render(request, 'ClubManager/home.html',
                      {'authenticated': True, 'all_transactions': all_transactions, 'profile': user_profile,
                       'to_settle': to_settle, 'error': error_message, 'success': success_message})
    else:
        if request.method == 'POST':
            if request.user.username == request.POST['username']:
                request.session["successful_club_rep_login"] = True
                return redirect(rep_dashboard)
            else:
                if request.session["club_rep_login_attempts"] >= 5:
                    logout(request)
                    return redirect('/')

                error_message = 'Invalid Rep ID, ' + str(5 - int(request.session["club_rep_login_attempts"])) \
                                + " attempts remaining."

                # Increment the users attempts.
                request.session["club_rep_login_attempts"] += 1

    return render(request, 'ClubManager/home.html', {'authenticated': False, 'error': error_message})


@login_required(login_url='/login/')
@allowed_users(allowed_roles='CinemaManager')
def view_clubs(request):
    # Lookup all clubs
    clubs = Club.objects.all()
    club_reps = UserProfile.objects.exclude(club__isnull=True)
    clubs_no_rep = Club.objects.filter(userprofile=None)

    return render(request, 'ClubManager/view_clubs.html',
                  {"clubs": clubs, "club_reps": club_reps, "clubs_no_rep": clubs_no_rep})


# View handling for registering a new club representative
@login_required(login_url='/login/')
@allowed_users(allowed_roles='CinemaManager')
def add_club(request):
    club_form = CreateClubForm()

    if request.method == 'POST':
        club_form = CreateClubForm(request.POST)

        if club_form.is_valid():
            club_form.save()
            return redirect(view_clubs)

    return render(request, 'ClubManager/add_club.html', {'club_form': club_form})


# The handler for the club information update page
@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
@allowed_users(allowed_roles='CinemaManager')
def delete_club(request, club_id):
    if club_id:
        lookup = Club.objects.get(id=club_id)
        lookup.delete()

    # Redirect back to the view clubs.
    return redirect(view_clubs)


# The handler for the club rep information update page
@login_required(login_url='/login/')
@allowed_users(allowed_roles='CinemaManager')
def update_club_rep(request, rep_id):
    if rep_id:
        lookup = UserProfile.objects.get(id=rep_id)
        form = CreateClubRepForm(request.POST or None, instance=lookup)

        if form.is_valid():
            form.save()
            return redirect(view_clubs)

        # Render the page.
        return render(request, 'ClubManager/update_rep.html', {'club_rep': lookup, 'form': form})

    # Redirect back to the homepage.
    return redirect(cinema_dashboard)


@login_required(login_url='/login/')
@allowed_users(allowed_roles='CinemaManager')
def delete_club_rep(request, rep_id):
    if rep_id:
        lookup = UserProfile.objects.get(id=rep_id)
        user_lookup = User.objects.get(id=lookup.user_obj.id)
        user_lookup.delete()

    # Redirect back to the view clubs.
    return redirect(view_clubs)


# View handling for registering a new club representative
@login_required(login_url='/login/')
@allowed_users(allowed_roles='CinemaManager')
def add_club_rep(request, club_id):
    lookup = Club.objects.get(id=club_id)
    club_rep_form = CreateClubRepForm()
    user_form = CreateUserForm()
    club_rep_form.id = club_id

    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        user_form.username = 'ClubRep'

        club_rep_form = CreateClubRepForm(request.POST)
        club_rep_form.fields['club'].initial = club_id

        if user_form.is_valid() and club_rep_form.is_valid():
            user = user_form.save()
            user.is_active = True  # Makes the account active

            club_rep = club_rep_form.save(commit=False)
            club_rep.club = lookup
            club_rep.user_obj = user
            club_rep.save()

            user.username = int(club_rep.id) + 1000
            user = user_form.save()
            setup_user(user, 'ClubRepresentative')

            return redirect(view_clubs)

    return render(request, 'ClubManager/add_rep.html', {'user_form': user_form, 'club_rep_form': club_rep_form})
