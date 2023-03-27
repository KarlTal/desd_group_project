from django.shortcuts import render


# The handler for the homepage of the website.
def home(request):
    return render(request, 'AccountManager/home.html', {})
