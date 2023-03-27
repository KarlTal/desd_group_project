from django import forms

from UWEFlix.models import Club
from .models import ClubRepProfile


class CreateClubRepForm(forms.ModelForm):
    class Meta:
        model = ClubRepProfile
        fields = ['clubID', 'dob', 'credit']


class CreateClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'street_number', 'street_name', 'city', 'postcode', 'landline', 'mobile', 'discount', 'email']
