from django.db import models

# The database class for the Clubs
from UWEFlix.models import User, Club


# The database class for the club representative
class ClubRepProfile(models.Model):
    repID = models.AutoField(primary_key=True)
    clubID = models.ForeignKey(Club, null=True, on_delete=models.CASCADE)  # is the relationship 1-1?
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    dob = models.DateField(auto_now_add=False, auto_now=False, blank=False)
    credit = models.PositiveIntegerField()
    autocomplete_fields = ['user']
