from django import forms
from UWEFlix.models import Club
from UWEFlix.models import UserProfile

class CreateClubRepForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['club', 'date_of_birth', 'credits']




class CreateClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'street_number', 'street_name', 'city', 'postcode', 'landline', 'mobile', 'discount', 'email']
