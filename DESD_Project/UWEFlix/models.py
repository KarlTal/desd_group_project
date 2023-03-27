from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, Group
from django.db import models
from django.utils import timezone


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        UserProfile.objects.get_or_create(user=user)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self._create_user(email, password, **extra_fields)
        set_user_group(user, 'Student')

        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        user = self._create_user(email, password, **extra_fields)
        set_user_group(user, 'AccountManager')

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Account information.
    email = models.EmailField(blank=True, default='', unique=True)
    username = models.CharField(max_length=150, blank=True, default='')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    # Django account information.
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        if not self.first_name or self.first_name == '':
            return self.email.split('@')[0]
        else:
            return self.first_name

    def get_profile(self):
        return UserProfile.objects.get_or_create(user=self)


# The database class for the Clubs available at UWEFlix
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


# The database class for the Films displayed at UWEFlix
class Film(models.Model):
    RATINGS = (('U', 'U'), ('PG', 'PG'), ('12A', '12A'), ('12', '12'), ('15', '15'), ('18', '18'))

    title = models.CharField(max_length=32)
    age_rating = models.CharField(max_length=5, choices=RATINGS)
    duration = models.IntegerField()
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='films/', null=True)

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


# The database class for the Tickets at UWEFlix.
class Ticket(models.Model):
    seat = models.IntegerField()
    showing = models.ForeignKey(Showing, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    club = models.ForeignKey(Club, null=True, on_delete=models.SET_NULL)
    price = models.FloatField()


# The database class for the club representative
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, null=True, on_delete=models.CASCADE)
    date_of_birth = models.DateField(auto_now_add=False, auto_now=False, blank=False)
    credit = models.PositiveIntegerField()
    autocomplete_fields = ['user']


# Create the user groups.
def setup_groups():
    Group.objects.get_or_create(name='AccountManager')
    Group.objects.get_or_create(name='CinemaManager')
    Group.objects.get_or_create(name='ClubRepresentative')
    Group.objects.get_or_create(name='Student')


def set_user_group(user, group_key):
    setup_groups()
    group = Group.objects.get(name=group_key)
    user.groups.add(group)
