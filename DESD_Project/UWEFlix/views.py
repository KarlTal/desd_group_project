from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .forms import *
from .decorators import *
from django.contrib.auth.decorators import login_required
# View handling for the UWEFlix homepage.
def home(request):
    return render(request, 'UWEFlix/home.html', {})


# View handling for user logins.
@unauthenticated_user
def login_user(request):
    error = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(home)
        else:
            error = "Invalid email or password!"

    return render(request, 'UWEFlix/login.html', {'error': error})


# View handling for user logging out.
@login_required
def logout_user(request):
    logout(request)
    return redirect(login_user)


# View handling for registering a new student.
@unauthenticated_user
def registerStudent(request):
    student_form = CreateStudentForm()
    user_form = CreateUserForm()
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        student_form = CreateStudentForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            group = Group.objects.get(name='student')
            user.groups.add(group)
            return redirect(login_user)
        else:
            print("Not valid")
    return render(request, 
                  'UWEFlix/register_student.html', 
                  {'user_form': user_form,'student_form':student_form})


# View handling for registering a new user.
@unauthenticated_user
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)

            return redirect(login_user)

    return render(request, 'UWEFlix/register.html', {'form': form})