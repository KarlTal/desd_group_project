from django import forms
from django.forms import ModelForm

from UWEFlix.forms import DateTimeLocalField
from UWEFlix.models import *


# The Form used when creating and editing Films available at UWEFlix.
class FilmForm(ModelForm):
    title = forms.TextInput()
    age_rating = forms.TextInput()
    duration = forms.NumberInput()
    description = forms.TextInput()

    # Specify the Meta so Django knows what fields we're modifying.
    class Meta:
        model = Film
        fields = ['title', 'age_rating', 'duration', 'description', 'image']


# The Form used to add Screens available.
class ScreenForm(ModelForm):
    capacity = forms.NumberInput()

    # Specify the Meta so Django knows what fields we're modifying.
    class Meta:
        model = Screen
        fields = ['capacity']


# The Form used to add and modify Screenings of Films.
class ShowingForm(ModelForm):
    time = DateTimeLocalField()

    # Specify the Meta so Django knows what fields we're modifying.
    class Meta:
        model = Showing
        fields = ['film', 'screen', 'time']
