from django.db import models

# The database class for the Clubs
from UWEFlix.models import User


class Club(models.Model):
    name = models.CharField(max_length=255)
    street_number = models.PositiveIntegerField()
    street_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    landline = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    discount = models.FloatField()
    email = models.EmailField()

    def __str__(self):
        return str(self.name)


# The database class for the club representative
class ClubRepProfile(models.Model):
    repID = models.AutoField(primary_key=True)
    clubID = models.ForeignKey(Club, null=True, on_delete=models.CASCADE)  # is the relationship 1-1?
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    dob = models.DateField(auto_now_add=False, auto_now=False, blank=False, )
    credit = models.PositiveIntegerField()
    autocomplete_fields = ['user']
