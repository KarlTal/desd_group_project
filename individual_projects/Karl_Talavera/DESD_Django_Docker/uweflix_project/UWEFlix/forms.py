from django import forms
from UWEFlix.models import LogMessage
from UWEFlix.models import Accounts
from UWEFlix.models import Clubs
from UWEFlix.models import ClubReps
from UWEFlix.models import Films


#CREATE (Register)
class RegisterFilmForm(forms.ModelForm):
    class Meta:

        model = Films
        fields = ('filmTitle','ageRating','duration','description','filmImages',)# NOTE: the trailing comma is required
        labels={
            "filmTitle" : "Enter film title",
            "ageRating":"Enter age rating",
            "duration":"Enter duration",
            "description":"Enter description",
            "filmImages":"Select film image",
            
        }

class RegisterAccountForm(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = ("username","password","firstName","surname","dateOfBirth","email",)
        labels={
            "username" : "Enter username",
            "password":"Enter password",
            "firstName":"Enter first name",
            "surname":"Enter surname",
            "dateOfBirth":"Enter date of birth",
            "email":"Enter email",
        }

#UPDATE

class UpdateFilmForm(forms.ModelForm):
    class Meta:
        model = Films
        fields = ('filmTitle','ageRating','duration','description','filmImages',)
        labels={
            "filmTitle" : "Enter film title",
            "ageRating":"Enter age rating",
            "duration":"Enter duration",
            "description":"Enter description",
            "filmImages":"Select film image",
            
        }
class UpdateAccountForm(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = ("username","password","firstName","surname","dateOfBirth","email",)
        labels={
            "username" : "Enter username",
            "password":"Enter password",
            "firstName":"Enter first name",
            "surname":"Enter surname",
            "dateOfBirth":"Enter date of birth",
            "email":"Enter email",
        }

#To be developed

# class RegisterClubsForm(forms.ModelForm):
#     class Meta:
#         model = Clubs
#         fields = ("clubName","street","city","postCode","landLineNumber","mobilePhoneNumber","clubEmailAddress","clubRepID",)
#         labels={
#             "filmTitle" : "Enter ",
#             "":"Enter ",
#             "":"Enter ",
#             "":"Enter ",
#             "":"Enter ",
            
#         }
# class RegisterClubRepsForm(forms.ModelForm):
#     class Meta:
#         model = ClubReps
#         fields = ("repNumber","clubPassword",)
#         labels={
#             "filmTitle" : "Film title",
#             "":"",
#             "":"",
#             "":"",
#             "":"",
            
#         }