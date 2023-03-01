from django.db import models
from django.utils import timezone
# Create your models here.

class LogMessage(models.Model):
    message =models.CharField(max_length=300)
    log_date = models.DateTimeField("date logged")

    def __str__(self):
        """Returns a string representation of a message"""
        date = timezone.localtime(self.log_date)
        return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}"


class Accounts(models.Model):
    #accountID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=300)
    password = models.CharField(max_length=300)
    firstName = models.CharField(max_length=300)
    surname = models.CharField(max_length=300)
    dateOfBirth = models.CharField(max_length=300)
    email = models.CharField(max_length=300)


class Clubs(models.Model):
    #clubID = models.AutoField(primary_key=True)
    clubName = models.CharField(max_length=300)
    street = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    postCode = models.CharField(max_length=10)
    landLineNumber = models.CharField(max_length=30)
    mobilePhoneNumber = models.CharField(max_length=30)
    clubEmailAddress = models.CharField(max_length=100)
    clubRepID = models.ForeignKey('ClubReps',on_delete=models.SET_DEFAULT,default=None)


class ClubReps(models.Model):
    #clubRepID = models.AutoField(primary_key=True)
    repNumber = models.PositiveBigIntegerField()
    clubPassword = models.CharField(max_length=300)


class Films(models.Model):

    AGE_RATING_CHOICES =(
        ('U','U'),
        ('PG','PG'),
        ('12A','12A'),
        ('15','15'),
        ('18','18'),
        ('R18','R18'),
    )

    filmTitle = models.CharField(max_length=300)
    ageRating = models.CharField(max_length=50,choices=AGE_RATING_CHOICES, default='green')
    duration = models.CharField(max_length=300)
    description = models.TextField()
    filmImages = models.ImageField(null=True, blank=True,upload_to='images/')

