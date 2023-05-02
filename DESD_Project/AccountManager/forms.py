from django import forms
from django.forms import ModelForm

from UWEFlix.forms import DateTimeLocalField
from UWEFlix.models import *


# The Form used when creating and editing Users.
class UserForm(ModelForm):
    email = forms.EmailField()
    username = forms.TextInput()
    first_name = forms.TextInput()
    last_name = forms.TextInput()
    is_active = forms.BooleanField()

    # Specify the Meta so Django knows what fields we're modifying.
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'is_active']


# The Form used when creating and editing User Profiles.
class UserProfileForm(ModelForm):
    date_of_birth = DateTimeLocalField()
    credits = forms.FloatField()
    discount = forms.IntegerField()

    # Specify the Meta so Django knows what fields we're modifying.
    class Meta:
        model = UserProfile
        fields = ['club', 'date_of_birth', 'credits', 'discount']
