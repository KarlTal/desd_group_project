from django.db import models

# This is the file in which the tables the database will comprise will be created
class UserDetails(models.Model):
    first_name = models.CharField(max_length = 100, default = "Adrian")
    last_name = models.CharField(max_length = 100, default = "Mitrea")
    date_of_birth = models.CharField(max_length = 100, default = "2nd September 2000")
    email = models.CharField(max_length = 100, default = "adrianmitrea20@yahoo.com")
    address = models.CharField(max_length = 100, default = "BS7 0JL")
    username = models.CharField(max_length = 20, default = "jane02")
    password = models.CharField(max_length = 15, default = "janedoe1234")

class FilmDetails(models.Model):
    film_name = models.CharField(max_length = 100, default = "Spiderman: No Way Home")
    film_description = models.CharField(max_length = 300, default = """With Spider-Man's identity now revealed, Peter asks Doctor Strange for help. When a spell 
                                                                        goes wrong, dangerous foes from other worlds start to appear, forcing Peter to discover what it truly means to be Spider-Man.""")
    film_duration = models.CharField(max_length = 30, default = "2h and 28 mins")
    film_age_rating = models.CharField(max_length = 50, default = "8+")
    film_release_date = models.CharField(max_length = 50, default = "15th December 2021")
    

