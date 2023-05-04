import uuid
from datetime import date

from django.shortcuts import render, redirect

from ClubManager.views import rep_dashboard
from UWEFlix.models import *
from UWEFlix.views import profile

# Global variable for our pending payments.
pending_payments = {}


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
            user_profile = UserProfile.objects.get(user_obj=request.user)
        except:
            user_profile = None

        club = None

        # If the user profile exists (e.g. logged in), then fetch the club and the users discount rate (if they have one).
        if user_profile is not None:
            club = user_profile.club
            discount = user_profile.discount

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
            elif showing.time < timezone.now():
                error_message = "This showing has already begin. Please choose another showing."
            else:
                unique_key = uuid.uuid4()

                student_price = student_ticket.price
                adult_price = adult_ticket.price
                child_price = child_ticket.price

                total_price = float((adult_quantity * adult_price) + (child_quantity * child_price) + (
                        student_quantity * student_price)) * (1 - (discount / 100))

                # If the current user is not logged in (e.g. they are a customer) then send them to the payment processing page.
                if request.user.is_anonymous:
                    pending_payments[str(unique_key)] = PendingBooking(showing_id, child_quantity, adult_quantity,
                                                                       student_quantity, total_price, 0)

                    return redirect('/booking/payment/' + str(unique_key))

                if club is None and total_price > user_profile.credits:
                    pending_payments[str(unique_key)] = PendingBooking(showing_id, child_quantity, adult_quantity,
                                                                       student_quantity, total_price,
                                                                       user_profile.credits)

                    return redirect('/booking/payment/' + str(unique_key))
                else:
                    has_been_paid = False

                    # Update the users credit.
                    if club is None:
                        user_profile.credits = user_profile.credits - total_price
                        user_profile.save()
                        has_been_paid = True

                    new_booking = Booking.objects.create(user_email=request.user.email, unique_key=unique_key,
                                                         showing=showing, date=date.today(),
                                                         total_price=total_price, ticket_count=total_quantity,
                                                         has_been_paid=has_been_paid)

                    for i in range(adult_quantity):
                        Ticket.objects.create(booking=new_booking, ticket_type=adult_ticket)
                    for i in range(child_quantity):
                        Ticket.objects.create(booking=new_booking, ticket_type=child_ticket)
                    for i in range(student_quantity):
                        Ticket.objects.create(booking=new_booking, ticket_type=student_ticket)

                    showing.seats_taken += total_quantity
                    showing.save()

                    # Register our credit transaction.
                    Transaction.objects.create(user_email=request.user.email, origin='Booking ' + str(new_booking.id), type='Credit', amount=total_price)

                    return redirect(confirmation, booking_id=new_booking.id, unique_key=unique_key)

        return render(request, 'BookingManager/book_film.html',
                      {'film': lookup, 'club': club, 'showing': showing, 'profile': user_profile,
                       'remaining_seats': remaining_seats, "adult_ticket": adult_ticket, "child_ticket": child_ticket,
                       "student_ticket": student_ticket, 'discount': discount, 'error': error_message})

    # Redirect back to the homepage.
    return redirect(home)


def payment(request, unique_key):
    pending_booking = pending_payments[unique_key]

    showing = Showing.objects.get(id=pending_booking.booking_id)
    error_message = ''

    if request.POST:
        email = request.POST.get('email')

        # Ensure we still have enough seats for this booking.
        total_quantity = pending_booking.total_tickets
        remaining_seats = showing.screen.capacity - showing.seats_taken

        if remaining_seats < total_quantity:
            error_message = "There are no longer enough seats available!"
        elif showing.time < timezone.now():
            error_message = "This showing has already begin. Please choose another showing."
        else:
            # Create the new booking.
            new_booking = Booking.objects.create(user_email=email, unique_key=unique_key, showing=showing,
                                                 date=date.today(),
                                                 total_price=pending_booking.price, ticket_count=total_quantity,
                                                 has_been_paid=True)

            if pending_booking.credits_used > 0:
                # Register our credit transaction.
                Transaction.objects.create(user_email=email, origin='Booking ' + str(new_booking.id), type='Credit',
                                           amount=pending_booking.credits_used)

                # Subtract the credits from the users profile.
                user_profile = UserProfile.objects.get(user_obj=User.objects.get(email=email))
                user_profile.credits = user_profile.credits - pending_booking.credits_used
                user_profile.save()

            # Create the new ticket objects and attribute them to the booking.
            for i in range(int(pending_booking.adult_tickets)):
                Ticket.objects.create(booking=new_booking, ticket_type=TicketType.objects.get(id=1))
            for i in range(int(pending_booking.child_tickets)):
                Ticket.objects.create(booking=new_booking, ticket_type=TicketType.objects.get(id=2))
            for i in range(pending_booking.student_tickets):
                Ticket.objects.create(booking=new_booking, ticket_type=TicketType.objects.get(id=3))

            # Increase the showings occupied seats.
            showing.seats_taken += total_quantity
            showing.save()

            # Register our debit transaction.
            Transaction.objects.create(user_email=email, origin='Booking ' + str(new_booking.id), type='Debit', amount=pending_booking.to_pay)

            return redirect(confirmation, booking_id=new_booking.id, unique_key=unique_key)

    return render(request, 'BookingManager/payment.html', {'booking': pending_booking, 'error': error_message})


def purchase(request, purchase_type, value):
    error_message = ''

    user_profile = UserProfile.objects.get(user_obj=request.user)

    if request.POST:
        # Validate that the email inputted is correct.
        if request.POST.get('email') == request.user.email:

            if purchase_type == 'top_up':
                amount = float(request.POST.get('credit_amount'))

                if amount <= 5:
                    error_message = 'Amount to top up must be greater than £5.00'
                else:
                    # Register our credit transaction.
                    Transaction.objects.create(user_email=request.user.email, origin='Credit Top Up', type='Debit', amount=amount)

                    # Top up club rep credits
                    user_profile.credits += amount
                    user_profile.save()

                    return redirect(profile)
        else:
            error_message = 'The email provided doesn\'t match your accounts!'

    return render(request, 'BookingManager/payment.html',
                  {'purchase_type': purchase_type, 'value': value, 'error': error_message})


def confirmation(request, booking_id, unique_key):
    booking = Booking.objects.get(id=booking_id)

    if str(unique_key) != str(booking.unique_key):
        return redirect(home)

    return render(request, 'BookingManager/confirmation.html', {'booking': booking})


def cancel_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)

    if request.user.email == booking.user_email:
        booking.pending_cancel = True
        booking.save()

    return redirect(confirmation, booking_id=booking.id, unique_key=booking.unique_key)


class PendingBooking:
    def __init__(self, booking_id, child_tickets, adult_tickets, student_tickets, price, credits_used):
        self.booking_id = booking_id
        self.child_tickets = child_tickets
        self.adult_tickets = adult_tickets
        self.student_tickets = student_tickets
        self.total_tickets = int(child_tickets) + int(adult_tickets) + int(student_tickets)
        self.price = price
        self.credits_used = credits_used
        self.to_pay = price - credits_used
