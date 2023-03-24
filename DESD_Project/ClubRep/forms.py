from .models import ClubRepProfile
from .models import Club
from django import forms

class CreateClubRepForm(forms.ModelForm):
    class Meta:
        model = ClubRepProfile
        fields = ['clubID','dob','credit']


class CreateClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name','street_number','street_name','city','postcode','landline','mobile','discount','email']


# class MakeBlockBooking(forms.ModelForm):
#     class Meta:
#         model = BlockBooking
#         fields = ['quantity']
        
