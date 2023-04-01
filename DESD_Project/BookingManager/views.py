import uuid
from datetime import date

from django.shortcuts import render, redirect

from UWEFlix.models import *
from UWEFlix.views import profile


def home(request):
    return redirect('/')


# Create your views here.
def book_film(request, film_id, showing_id):
    if film_id and showing_id:
        error_message = ''

        lookup = Film.objects.get(id=film_id)
        showing = Showing.objects.get(id=showing_id)

        adult_ticket = TicketType.objects.get(id=1)
        child_ticket = TicketType.objects.get(id=2)
        student_ticket = TicketType.objects.get(id=3)
        discount = 0

        # Wrap with try catch as if the user is not logged in (e.g. a Customer) then this will error.
        try:
            profile = UserProfile.objects.get(user_obj=request.user)
        except:
            profile = None

        club = None

        # If the user profile exists (e.g. logged in), then fetch the club and the users discount rate (if they have one).
        if profile is not None:
            club = profile.club
            discount = profile.discount

        # If the club exists, set the current discount to the club discount if it is bigger than the current user discount.
        if club is not None:
            if club.discount > discount:
                discount = club.discount

        remaining_seats = showing.screen.capacity - showing.seats_taken

        if request.POST:
            student_quantity = int(request.POST["student_quantity"])
            adult_quantity = int(request.POST["adult_quantity"])
            child_quantity = int(request.POST["child_quantity"])
            total_quantity = student_quantity + adult_quantity + child_quantity

            if total_quantity <= 0:
                error_message = "You must book at least 1 seat!"
            elif remaining_seats < total_quantity:
                error_message = "There are not enough seats available for this many tickets! (1)"
            else:
                # If the current user is not logged in (e.g. they are a customer) then send them to the payment processing page.
                if request.user.is_anonymous:
                    return redirect(
                        '/booking/payment/' + str(showing_id) + ":" + str(adult_quantity) + ":" + str(child_quantity))

                student_price = student_ticket.price
                adult_price = adult_ticket.price
                child_price = child_ticket.price

                total_price = float((adult_quantity * adult_price) + (child_quantity * child_price) + (
                        student_quantity * student_price)) * (1 - (discount / 100))

                if total_price > profile.credits:
                    error_message = "You do not have sufficient credit for this purchase!"
                else:
                    # Update the users credit.
                    profile.credits = profile.credits - total_price
                    profile.save()

                    unique_key = uuid.uuid4()

                    new_booking = Booking.objects.create(user_email=request.user.email, unique_key=unique_key,
                                                         showing=showing, date=date.today(),
                                                         total_price=total_price, ticket_count=total_quantity)

                    for i in range(adult_quantity):
                        Ticket.objects.create(booking=new_booking, ticket_type=adult_ticket)
                    for i in range(child_quantity):
                        Ticket.objects.create(booking=new_booking, ticket_type=child_ticket)
                    for i in range(student_quantity):
                        Ticket.objects.create(booking=new_booking, ticket_type=student_ticket)

                    showing.seats_taken += total_quantity
                    showing.save()

                    return redirect(confirmation, booking_id=new_booking.id, unique_key=unique_key)

        return render(request, 'BookingManager/book_film.html',
                      {'film': lookup, 'club': club, 'showing': showing, 'remaining_seats': remaining_seats,
                       "adult_ticket": adult_ticket, "child_ticket": child_ticket, "student_ticket": student_ticket,
                       'discount': discount, 'error': error_message})

    # Redirect back to the homepage.
    return redirect(home)


def payment(request, showing_id, adult, child):
    showing = Showing.objects.get(id=showing_id)
    error_message = ''

    if request.POST:
        email = request.POST.get('email')

        adult_ticket = TicketType.objects.get(id=1)
        child_ticket = TicketType.objects.get(id=2)

        total_quantity = int(adult) + int(child)
        remaining_seats = showing.screen.capacity - showing.seats_taken

        print(remaining_seats, total_quantity)

        if remaining_seats < total_quantity:
            error_message = "There are no longer enough seats available!"
        else:
            total_price = float((int(adult) * adult_ticket.price) + (int(child) * child_ticket.price))
            unique_key = uuid.uuid4()

            new_booking = Booking.objects.create(user_email=email, unique_key=unique_key, showing=showing,
                                                 date=date.today(),
                                                 total_price=total_price, ticket_count=total_quantity)

            for i in range(int(adult)):
                Ticket.objects.create(booking=new_booking, ticket_type=adult_ticket)
            for i in range(int(adult)):
                Ticket.objects.create(booking=new_booking, ticket_type=child_ticket)

            showing.seats_taken += total_quantity
            showing.save()

            return redirect(confirmation, booking_id=new_booking.id, unique_key=unique_key)

    return render(request, 'BookingManager/payment.html', {'error': error_message})


def confirmation(request, booking_id, unique_key):
    booking = Booking.objects.get(id=booking_id)

    if str(unique_key) != str(booking.unique_key):
        return redirect(home)

    return render(request, 'BookingManager/confirmation.html', {'booking': booking})


def cancel_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)

    if request.user.email == booking.user_email:
        booking.delete()

        # Reduce the number of seats taken.
        showing = booking.showing
        showing.seats_taken = showing.seats_taken - booking.ticket_count
        showing.save()

    return redirect(profile)
