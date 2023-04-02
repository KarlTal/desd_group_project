from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from UWEFlix.decorators import allowed_users


# The handler for the homepage of the website.
@login_required(login_url='/login')
@allowed_users(allowed_roles='AccountManager')
def home(request):
    return render(request, 'AccountManager/home.html', {})
