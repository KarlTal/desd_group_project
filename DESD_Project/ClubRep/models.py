from django.db import models

# The database class for the Clubs
from CinemaManager.models import Showing
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


# Booking system
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    showing = models.ForeignKey(Showing, on_delete=models.SET_NULL, null=True)  # Add showings
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField(blank=True, default=0.5)  # Change later


class Ticket(models.Model):
    booking_id = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True)
    price = models.FloatField()
    seat = models.CharField(max_length=3)

# class BlockBooking(models.Model):
#     repID = models.ForeignKey(ClubRepProfile, on_delete=models.SET_NULL,null=True)
#     quantity = models.PositiveIntegerField()
#     showing = models.ForeignKey(Showing,on_delete=models.SET_NULL, null=True)#Add showings
#     date = models.DateTimeField(auto_now_add=True)
#     total_price = models.FloatField
