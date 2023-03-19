from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student
from django import forms

# Form responsible for handling the creation of UWEFlix users.
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']


class CreateStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['pending']