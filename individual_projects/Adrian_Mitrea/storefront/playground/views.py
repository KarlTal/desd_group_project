from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# View function: It takes a request and returns a response (Request -> response)
# Request handler (View - name is misleading)

def say_hello(request):

    # With this function we can:
    # a) Pull data from a database
    # b) Transform data
    # c) Send emails

    return render(request, "hello.html", {"name": "Adrian"})

