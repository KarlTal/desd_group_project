from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from CinemaManager.views import cinema_dashboard
from UWEFlix.models import *
from .decorators import *
from .forms import *
from datetime import date


# View handling for the UWEFlix homepage.
def home(request):
    films = Film.objects.all()
    return render(request, 'UWEFlix/home.html', {'films': films})


def film(request, film_id):
    # If the film_id exists and the form is valid, update the Film database object with the data from the form.
    if film_id:
        lookup = Film.objects.get(id=film_id)
        showings = Showing.objects.filter(film=lookup)

        # Render the page.
        return render(request, 'UWEFlix/film.html', {'film': lookup, 'showings': showings})

    # Redirect back to the homepage.
    return redirect(home)


def booking(request, film_id, showing_id):
    if film_id and showing_id:
        lookup = Film.objects.get(id=film_id)
        showing = Showing.objects.get(id=showing_id)
        
        student_price = 5.99
        adult_price = 6.99
        child_price = 4.99


        if request.POST:

            if request.user.is_authenticated:
                student_quantity=request.POST["student_quantity"]

                if showing.screen.capacity - showing.seats_taken < int(student_quantity):
                    error_message = "Not enough available seats"

                    return render(request, 'UWEFlix/booking.html', {'film': lookup, 'showing': showing, "error_message":error_message})
                else:
                    total_price = float(int(student_quantity) * student_price)
                    bookingObj = Booking.objects.create(user_email=request.user.email,showing=showing,date=date.today(),total_price =total_price,ticket_count=int(student_quantity))
                    
                    for student in range(int(student_quantity)):
                        Ticket.objects.create(booking=bookingObj,ticket_type="Student", price=student_price)

                    showing.seats_taken +=student_quantity
                    showing.save()
                    
                    return redirect(home)
                    
            else:
                user_email = request.POST["user_email"]
                adult_quantity = request.POST["adult_quantity"]
                child_quantity = request.POST["child_quantity"]
                total_quantity = int(adult_quantity) + int(child_quantity)

                if showing.screen.capacity - showing.seats_taken < total_quantity:
                    error_message = "Not enough available seats"

                    return render(request, 'UWEFlix/booking.html', {'film': lookup, 'showing': showing, "error_message":error_message})
                else:
                    total_price = float(int(adult_quantity) * adult_price + (int(child_quantity) * child_price))
                    bookingObj = Booking.objects.create(user_email=user_email,showing=showing,date=date.today(),total_price =total_price,ticket_count=int(total_quantity))
                    
                    for i in range(int(adult_quantity)):
                        Ticket.objects.create(booking=bookingObj,ticket_type="Adult", price=adult_price)
                    
                    for i in range(int(child_quantity)):
                        Ticket.objects.create(booking=bookingObj,ticket_type="Child", price=child_price)
                    
                    showing.seats_taken +=total_quantity
                    showing.save()

                    return redirect(home)
                
        return render(request, 'UWEFlix/booking.html', {'film': lookup, 'showing': showing})
    # Redirect back to the homepage.
    return redirect(home)






# View handling for user logins.
@unauthenticated_user
def login_user(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            group = request.user.groups.all()[0].name

            if "CinemaManager" in group:
                return redirect(cinema_dashboard)
            elif 'Student' in group:
                if not request.user.is_active:
                    logout(request)
                    error = "Your student account has not yet been approved!"
                else:
                    return redirect(home)
            else:
                return redirect(home)
        else:
            error = "Invalid email/username or password!"

    return render(request, 'UWEFlix/login.html', {'error': error})


# View handling for user logging out.
@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    return redirect(login_user)


# View handling for registering a new user.
@unauthenticated_user
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            set_user_group(form.save(), 'Student')
            return redirect(login_user)

    return render(request, 'UWEFlix/register.html', {'form': form})
