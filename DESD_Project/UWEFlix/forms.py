from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Form responsible for handling the creation of UWEFlix users.
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']
