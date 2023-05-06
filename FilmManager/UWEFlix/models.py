from django.db import models


# Create your models here.

# The database class for the Films displayed at UWEFlix
class Film(models.Model):
    title = models.CharField(max_length=32)
    age_rating = models.CharField(max_length=5)
    duration = models.IntegerField()
    description = models.CharField(max_length=255)

    image = models.ImageField(null=True)
    trailer = models.CharField(max_length=255, null=True)

    class Meta:
        app_label = 'UWEFlix'

    def __str__(self):
        return self.title
