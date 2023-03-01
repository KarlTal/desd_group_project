from django.shortcuts import render
import re 
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect



def home(request):
    return render(request, 'UWEFlix/home.html')
