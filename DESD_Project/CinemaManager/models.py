from django.db import models
from django.utils import timezone


# The database class for the Films displayed at UWEFlix
class Film(models.Model):
    RATINGS = (('U', 'U'), ('PG', 'PG'), ('12A', '12A'), ('12', '12'), ('15', '15'), ('18', '18'))

    title = models.CharField(max_length=32)
    age_rating = models.CharField(max_length=5, choices=RATINGS)
    duration = models.IntegerField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.title


# The database class for the Screens at UWEFlix
class Screen(models.Model):
    screen_id = models.AutoField(primary_key=True)
    capacity = models.IntegerField()

    def __str__(self):
        return "Screen " + str(self.screen_id) + " (Capacity: " + str(self.capacity) + ")"


# The database class for the Showings at UWEFlix
class Showing(models.Model):
    film = models.ForeignKey(Film, null=True, on_delete=models.SET_NULL)
    screen = models.ForeignKey(Screen, null=True, on_delete=models.SET_NULL)
    time = models.DateTimeField(default=timezone.now)