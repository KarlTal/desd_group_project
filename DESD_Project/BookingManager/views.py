import decimal
from datetime import date

from django.shortcuts import render, redirect

from UWEFlix.models import *


def home(request):
    return redirect('/')


# Create your views here.
def book_film(request, film_id, showing_id):
    if film_id and showing_id:
        error_message = ''

        lookup = Film.objects.get(id=film_id)
        showing = Showing.objects.get(id=showing_id)
        club = None

        # Wrap with try catch as if the user is not logged in (e.g. a Customer) then this will error.
        try:
            profile = UserProfile.objects.get(user_obj=request.user)
        except UserProfile.DoesNotExist:
            profile = None

        if profile is not None:
            club = profile.club

        remaining_seats = showing.screen.capacity - showing.seats_taken
        
        if request.POST:

            if request.user.is_anonymous:
                # TODO: Add 'payment processing' page for Customers
                return redirect('/')

            student_price = showing.student_cost
            adult_price = showing.adult_cost
            child_price = showing.child_cost

            if club is not None:
                student_price = student_price * decimal.Decimal((1 - (club.discount / 100)))

            student_quantity = int(request.POST["student_quantity"])
            adult_quantity = int(request.POST["adult_quantity"])
            child_quantity = int(request.POST["child_quantity"])
            total_quantity = student_quantity + adult_quantity + child_quantity

            if total_quantity <= 0:
                error_message = "You must book at least 1 seat!"
            elif remaining_seats < total_quantity:
                error_message = "There are not enough seats available for this many tickets!"
            else:
                total_price = float((adult_quantity * adult_price) + (child_quantity * child_price) + (
                        student_quantity * student_price))

                if total_price > profile.credits:
                    error_message = "You do not have sufficient credit for this purchase!"
                else:
                    # Update the users credit.
                    profile.credits = profile.credits - total_price
                    profile.save()

                    new_booking = Booking.objects.create(user_email=request.user.email, showing=showing, date=date.today(),
                                                         total_price=total_price, ticket_count=total_quantity)

                    for i in range(adult_quantity):
                        Ticket.objects.create(booking=new_booking, ticket_type="Adult", price=adult_price)
                    for i in range(child_quantity):
                        Ticket.objects.create(booking=new_booking, ticket_type="Child", price=child_price)
                    for i in range(student_quantity):
                        Ticket.objects.create(booking=new_booking, ticket_type="Student", price=student_price)

                    showing.seats_taken += total_quantity
                    showing.save()

                    return redirect(home)

        return render(request, 'BookingManager/book_film.html',
                      {'film': lookup, 'club': club, 'showing': showing, 'remaining_seats': remaining_seats,
                       'error': error_message})

    # Redirect back to the homepage.
    return redirect(home)
