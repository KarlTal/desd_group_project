from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


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
