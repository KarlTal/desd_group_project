from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from AccountManager.forms import *
from UWEFlix.decorators import allowed_users
from UWEFlix.forms import get_form_errors


# The handler for the homepage of the account manager dashboard.
@login_required(login_url='/login/')
@allowed_users(allowed_roles='AccountManager')
def home(request):
    users = User.objects.all()
    profiles = UserProfile.objects.all()
    return render(request, 'AccountManager/home.html', {'users': users, 'profiles': profiles})


# Handle editing users.
@login_required(login_url='/login/')
@allowed_users(allowed_roles='AccountManager')
def update_user(request, user_id):
    error_message = ''

    # If the showing_id exists and the form is valid, update the Showing database object with the data from the form.
    if user_id:
        user_lookup = User.objects.get(id=user_id)
        profile_lookup = UserProfile.objects.get(user_obj=user_lookup)

        if user_lookup and profile_lookup:

            # Create the forms for modifying the users details.
            user_form = UserForm(request.POST or None, instance=user_lookup)
            profile_form = UserProfileForm(request.POST or None, instance=profile_lookup)

            # If the forms are valid e.g. they've been updated, then update the user details.
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect(home)
            else:
                error_message += get_form_errors(user_form)
                error_message += get_form_errors(profile_form)

            # Collect the users account statements.
            account_statements = {}

            transactions = Transaction.objects.filter(user_email=user_lookup.email)
            now = timezone.now()

            # Iterate through all of our transactions to collect the statements that exist.
            for transaction in transactions:
                year = transaction.date.year
                month = transaction.date.month

                # Ignore statements from invalid months.
                if year == now.year and month >= now.month:
                    continue

                key = (year, month)

                if key not in account_statements:
                    account_statements[key] = AccountStatement(year, month, [])

                account_statements[key].transactions.append(transaction)

            # Render the page.
            return render(request, 'AccountManager/update_user.html', {'user': user_lookup, 'profile': profile_lookup,
                                                                       'user_form': user_form, 'error': error_message,
                                                                       'profile_form': profile_form,
                                                                       'statements': account_statements.values()})

    # Redirect back to the homepage.
    return redirect(cinema_dashboard)


# The handler for deleting a user.
@login_required(login_url='/login/')
@allowed_users(allowed_roles='AccountManager')
def delete_user(request, user_id):
    # If a user_id is provided, lookup the User object and delete it.
    if user_id:
        lookup = User.objects.get(user=user_id)
        lookup.delete()

    # Redirect back to the homepage.
    return redirect(home)


# The handler for viewing a statement.
@login_required(login_url='/login/')
@allowed_users(allowed_roles='AccountManager')
def view_statement(request, email, year, month):
    transactions = Transaction.objects.filter(user_email=email)
    filtered_transactions = []

    # Filter the transactions only for the month and year we are viewing.
    for transaction in transactions:
        if transaction.date.year == int(year) and transaction.date.month == int(month):
            filtered_transactions.append(transaction)

    return render(request, 'AccountManager/view_statement.html',
                  {'email': email, 'year': year, 'month': month, 'period': get_statement_period(year, month),
                   'transactions': filtered_transactions})


# The handler for downloading a statement.
@login_required(login_url='/login/')
@allowed_users(allowed_roles='AccountManager')
def download_statement(request, email, year, month):
    transactions = Transaction.objects.filter(user_email=email)
    filtered_transactions = []

    # Filter the transactions only for the month and year we are viewing.
    for transaction in transactions:
        if transaction.date.year == int(year) and transaction.date.month == int(month):
            filtered_transactions.append(transaction)

    content = f"User email: {email}\n" \
              f"Period: {get_statement_period(year, month)}\n" \
              f"\nTransactions:\n"

    for transaction in filtered_transactions:
        formatted_datetime = transaction.date.strftime("%Y-%m-%d %H:%M:%S")
        content += f"{formatted_datetime} -- {transaction.origin} -- £{round(transaction.amount, 2)} -- {transaction.type}\n"

    # Create an HTTP response with the content and appropriate headers for downloading
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{email}_statement_{year}_{month}.txt"'

    return response


def get_statement_period(year, month):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]

    # Produce a string to demonstrate the period the statement is from.
    start_year = year
    start_month = None

    if int(month) <= 1:
        start_year = int(year) - 1
        start_month = 'December'
    else:
        start_month = months[int(month) - 2]

    return start_month + " " + str(start_year) + " - " + months[int(month) - 1] + " " + str(year)


class AccountStatement:
    def __init__(self, year, month, transactions):
        self.year = year
        self.month = month
        self.transactions = transactions
