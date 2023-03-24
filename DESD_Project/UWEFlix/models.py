from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, Group
from django.db import models
from django.utils import timezone


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
    email = models.EmailField(blank=True, default='', unique=True)

    username = models.CharField(max_length=150, blank=True, default='')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

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
