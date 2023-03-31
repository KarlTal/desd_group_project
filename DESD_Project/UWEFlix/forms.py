from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.forms import UserCreationForm
from UWEFlix.models import UserProfile
from .models import User
from django import forms

# Form responsible for handling the creation of UWEFlix users.
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

class CreateStudentForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = []

class UWEFlixBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()

        # First, test if the inputted username is the email.
        try:
            user = user_model.objects.get(email=username)
        except user_model.DoesNotExist:
            print("Failed to find account with provided email: " + username)
        else:
            if user.check_password(password):
                return user

        # Secondly, test if the inputted username is the username.
        try:
            user = user_model.objects.get(username=username)
        except user_model.DoesNotExist:
            print("Failed to find account with provided username: " + username)
        else:
            if user.check_password(password):
                return user

        return None
