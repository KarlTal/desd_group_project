from django.contrib.auth import logout,authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from CinemaManager.views import cinema_dashboard
from UWEFlix.decorators import *
from UWEFlix.forms import *
from UWEFlix.models import *
from .forms import *
from datetime import datetime
from django.db.models import Sum

# The handler for the homepage of the website.
@login_required(login_url='/login')
@allowed_users(allowed_roles='ClubRepresentative')
def rep_dashboard(request):
    request.session["club_rep_login_attempts"] = 0
    return render(request, 'ClubManager/home.html', {})


@login_required(login_url='login')
@allowed_users(allowed_roles='ClubRepresentative')
def view_transactions(request):
    error_message = ''
    context = {'version' : 1}
    group = get_group(request.user)

    # If the current user is an administrator, just display all the transactions.
    if group == 'Administrator':
        month_transactions = Booking.objects.filter(
            date__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0))
        all_transactions = Booking.objects.all().order_by('date')

        return render(request, 'ClubManager/view_transactions.html', {"month_transactions": month_transactions,
                                                                      "all_transactions": all_transactions})
    else:
        # Otherwise, only display the current club reps translations if they input their rep id correctly.
        if request.method == 'POST':
            if request.user.username == request.POST['username']:
                request.session["club_rep_login_attempts"] = 0

                # Gets all the bookings associated with the user's email
                month_transactions = Booking.objects.filter(
                    user_email=request.user.email,
                    date__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                )

                all_transactions = Booking.objects.filter(user_email=request.user.email).order_by('date')

                return render(request, 'ClubManager/view_transactions.html', {"month_transactions": month_transactions,
                                                                              "all_transactions": all_transactions})
            else:
                if request.session["club_rep_login_attempts"] >= 5:
                    logout(request)
                    return redirect('/')

                error_message = 'Invalid Rep ID, ' + str(5 - int(request.session["club_rep_login_attempts"])) \
                                + " attempts remaining."

                request.session["club_rep_login_attempts"] += 1

                context = {'error':error_message,
                           'version' : 1
                           }

        return render(request, 'ClubManager/club_rep_verify.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles='ClubRepresentative')
def settle_transactions_monthly(request):
    error_message = ''
    context = {
        'success': "All monthly transactions have been settled"
    }
    #Check if the current club rep has enough credits to settle the amount
    user = request.user
    club_rep = UserProfile.objects.get(user_obj=user)
    #Check the transactions of the current month
    monthly_transactions = Booking.objects.filter(Q(user_email=user.email)&Q(date__month=datetime.today().month)&Q(has_been_paid=False))
    print(monthly_transactions)
    if len(monthly_transactions)>0:
        #Count total sum of all the transactions
        total_transactions_price = monthly_transactions.aggregate(Sum('total_price'))
        if total_transactions_price.get('total_price__sum') > club_rep.credits:
            error_message = "You do not have enough credits to settle montly transaction"
            context = {
                'error': error_message,
                'version' : 2,
                'top_up_credits':True,
                'available_credits':club_rep.credits,
                'total_transactions_price':total_transactions_price.get('total_price__sum'),
                'club_rep_id':club_rep.id
            }
            return render(request, 'ClubManager/club_rep_verify.html', context)
        else:
            if request.method == 'POST':

                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    request.session["club_rep_login_attempts"] = 0
                    for booking in monthly_transactions:
                        booking.has_been_paid = True
                        booking.save()
                    #Deduct from club rep's credits
                    club_rep.credits -= total_transactions_price.get('total_price__sum')
                    club_rep.save()
                    return redirect(rep_dashboard)

                else:
                    if request.session["club_rep_login_attempts"] >= 5:
                        logout(request)
                        return redirect('/') 

                    error_message = 'Invalid Credentials, ' + str(5 - int(request.session["club_rep_login_attempts"])) \
                                    + " attempts remaining."

                    request.session["club_rep_login_attempts"] += 1
                    context ={'error':error_message,
                            'version' : 2
                            }
            
            return render(request, 'ClubManager/club_rep_verify.html', context)
    else:
        return render(request, 'ClubManager/club_rep_verify.html', context)

# The handler for topping up the exact amount of credits for settling the monthly transaction
@login_required(login_url='login')
@allowed_users(allowed_roles='ClubRepresentative')
def top_up_credits(request,type):
    user = request.user
    club_rep = UserProfile.objects.get(user_obj=user)
    error_message = ''
    context = {}

    if int(type) == 1:
        print("nay")
        monthly_transactions = Booking.objects.filter(Q(user_email=user.email)&Q(date__month=datetime.today().month)&Q(has_been_paid=False))
        total_transactions_price = monthly_transactions.aggregate(Sum('total_price'))
        credits_needed = total_transactions_price.get('total_price__sum') - club_rep.credits
        context = {
            'credits_needed': credits_needed
        }
        if request.POST:
            if request.POST.get('email') == user.email:
                for booking in monthly_transactions:
                    booking.has_been_paid = True
                    booking.save()
                #Top up club rep credits
                club_rep.credits += credits_needed
                club_rep.save()
                #Deduct from club rep's credits
                club_rep.credits -= total_transactions_price.get('total_price__sum')
                club_rep.save()
                return redirect(settle_transactions_monthly)
            else:
                error_message = 'Incorrect Email Address'
                context = {
                    'credits_needed': credits_needed,
                    'error':error_message
                }
                return render(request, 'BookingManager/payment.html', context)
        return render(request, 'BookingManager/payment.html', context)
    elif int(type) == 2:
        context = {
            'version': 2,
        }
        if request.POST:
                if request.POST.get('email') == user.email:
                    amount = float(request.POST.get('credit_amount'))
                    if amount <= 5:
                        error_message = 'Amount to top up must be greater than £5.00'
                        context = {
                            'error':error_message
                        }
                        return render(request, 'BookingManager/payment.html', context)
                    #Top up club rep credits    
                    club_rep.credits += amount
                    club_rep.save()
                    return redirect(rep_dashboard)

                else:
                    error_message = 'Incorrect Email Address'
                    context = {
                        'error':error_message
                    }
                    return render(request, 'BookingManager/payment.html', context)
        return render(request, 'BookingManager/payment.html', context)

# The handler for topping up the club rep's credit by a specific amount
# @login_required(login_url='login')
# @allowed_users(allowed_roles='ClubRepresentative')
# def top_up(request):
#     user = request.user
#     club_rep = UserProfile.objects.get(user_obj=user)
#     error_message = ''
#     if request.POST:
#             if request.POST.get('email') == user.email:
#                 amount = request.POST.get('amount')
#                 #Top up club rep credits
#                 club_rep.credits += amount
#                 club_rep.save()
#                 return redirect(rep_dashboard)
#             else:
#                 error_message = 'Incorrect Email Address'
#                 context = {
#                     'error':error_message
#                 }
#                 return render(request, 'BookingManager/payment.html', context)
#     return render(request, 'BookingManager/payment.html', context)

@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def view_clubs(request):
    # Lookup all clubs
    clubs = Club.objects.all()
    club_reps = UserProfile.objects.exclude(club__isnull=True)
    clubs_with_no_club_reps = Club.objects.filter(userprofile=None)

    return render(request, 'ClubManager/view_clubs.html',
                  {"clubs": clubs, "club_reps": club_reps, "clubs_with_no_club_reps": clubs_with_no_club_reps})


@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def view_club_reps(request):
    # Lookup all club reps
    club_reps = UserProfile.objects.exclude(club__isnull=True)
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

    return render(request, 'ClubManager/add_club.html', {'club_form': club_form})


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
    return redirect(cinema_dashboard)


@login_required(login_url='/login')
@allowed_users(allowed_roles='CinemaManager')
def delete_club_rep(request, rep_id):
    if rep_id:
        lookup = UserProfile.objects.get(id=rep_id)
        user_lookup = User.objects.get(id=lookup.user_obj.id)
        user_lookup.delete()

    # Redirect back to the view clubs.
    return redirect(view_club_reps)


# View handling for registering a new club representative
@login_required(login_url='/login')
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

            return redirect(view_club_reps)

    return render(request, 'ClubManager/add_rep.html', {'user_form': user_form, 'club_rep_form': club_rep_form})
