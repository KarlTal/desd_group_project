from django import forms
from cinemaBookingSystem.models import UserDetails

class UpdateForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ("first_name", "last_name", "date_of_birth", "username", "password", "address", "email", )
        labels = {
            "first_name":"First Name",
            "last_name" : "Last Name",
            "date_of_birth" : "Date of birth",
            "username" : "Username",
            "password" : "Password",
            "email" : "Email",
            "address" : "Address",
        }