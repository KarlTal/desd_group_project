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

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self._create_user(email, password, **extra_fields)
        setup_user(user, 'Student')

        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        user = self._create_user(email, password, **extra_fields)
        setup_user(user, 'Administrator')

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


# The database class for the Clubs available at UWEFlix
class Club(models.Model):
    name = models.CharField(max_length=255)
    street_number = models.PositiveIntegerField()
    street_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    landline = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    discount = models.IntegerField()
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
    image = models.ImageField(upload_to='Assets/', null=True)

    def __str__(self):
        return self.title


# The database class for the Screens at UWEFlix
class Screen(models.Model):
    screen_id = models.AutoField(primary_key=True)
    capacity = models.IntegerField()

    def __str__(self):
        return "Screen " + str(self.screen_id)


# The database class for the Showings at UWEFlix
class Showing(models.Model):
    film = models.ForeignKey(Film, null=True, on_delete=models.SET_NULL)
    screen = models.ForeignKey(Screen, null=True, on_delete=models.SET_NULL)
    time = models.DateTimeField(default=timezone.now)
    seats_taken = models.IntegerField(default=0)

    def __str__(self):
        return "Showing (" + str(self.film.title) + ")"


# The database class for Ticket Bookings.
class Booking(models.Model):
    user_email = models.EmailField(null=True)
    unique_key = models.UUIDField(null=True)

    club = models.ForeignKey(Club, null=True, blank=True, on_delete=models.SET_NULL)
    showing = models.ForeignKey(Showing, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(default=timezone.now)

    total_price = models.FloatField(default=0)
    ticket_count = models.IntegerField(default=0)
    has_been_paid = models.BooleanField(default=False)
    pending_cancel = models.BooleanField(default=False)

    def __str__(self):
        return "Booking (" + str(self.showing.film.title) + ")"


# The database model of ticket types.
class TicketType(models.Model):
    ticket_name = models.CharField(max_length=7, null=True, blank=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.ticket_name + " Ticket"


# The database class for the Tickets.
class Ticket(models.Model):
    booking = models.ForeignKey(Booking, null=True, on_delete=models.SET_NULL)
    ticket_type = models.ForeignKey(TicketType, null=True, on_delete=models.CASCADE)


# The database class for user profiles.
class UserProfile(models.Model):
    user_obj = models.OneToOneField(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, null=True, on_delete=models.CASCADE, blank=True)
    date_of_birth = models.DateField(default=timezone.now, auto_now_add=False, auto_now=False, blank=False)

    credits = models.FloatField(default=0)
    discount = models.IntegerField(null=True, blank=True, default=0)
    applied_discount = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.user_obj.email + "'s Profile"


# The database class for users statements.
class Transaction(models.Model):
    TYPES = (('Debit', 'Debit'), ('Credit', 'Credit'))

    user_email = models.EmailField(null=True)
    type = models.CharField(max_length=6, choices=TYPES)
    amount = models.FloatField(default=0)
    date = models.DateTimeField(default=timezone.now)


# Create the user groups.
def setup_groups():
    Group.objects.get_or_create(name='AccountManager')
    Group.objects.get_or_create(name='CinemaManager')
    Group.objects.get_or_create(name='ClubRepresentative')
    Group.objects.get_or_create(name='Student')
    Group.objects.get_or_create(name='Administrator')


def setup_user(user, group_key):
    # Ensure that the websites groups have been created.
    setup_groups()

    # Assign the user to their designated group.
    group = Group.objects.get(name=group_key)
    user.groups.add(group)

    # Create the users profile.
    UserProfile.objects.get_or_create(user_obj=user)


def get_group(user):
    return user.groups.all()[0].name
