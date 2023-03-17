from django.shortcuts import render

from .forms import *
from .models import *

# The handler for the homepage of the website.
def home(request):
    return render(request, 'AccountManager/home.html', {})