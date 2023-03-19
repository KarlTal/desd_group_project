from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db import models
from django.contrib.auth.models import User
# Overriding model for handling user authentication. Instead of checking that the username matches, we check that
# the email matches.
class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
        except user_model.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None


class Student(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    pending = models.BooleanField(default = 0)



     
