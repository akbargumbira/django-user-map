# coding=utf-8
from django.contrib.gis.db import models
from django.contrib.gis.db.models import GeoManager
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager, GeoManager):
    """Custom user manager for user map."""
    def create_user(
            self, name, email, location, email_updates, role, password=None):
        """Creates and saves a User.

        :pa
        :param email:
        :param password:
        """
        if not name:
            raise ValueError('Users must have name.')

        if not email:
            raise ValueError('Users must have an email address.')

        if not location:
            raise ValueError('Users must have location.')

        if not email_updates:
            raise ValueError('Users must have email updates status.')

        if not role:
            raise ValueError('Users must have role.')

        user = self.model(
            name=name,
            email=self.normalize_email(email),
            location=location,
            email_updates=email_updates,
            role=role
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password):
        """
        Creates and saves a superuser.

        :param email:
        :param password:
        """
        # Use fake role and location for superuser
        role = Role(
            name="Super User",
            sort_number=99)
        role.save()

        location = 'POINT(144 5)'

        user = self.create_user(
            name,
            email,
            location=location,
            email_updates=True,
            role=role,
            password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class Role(models.Model):
    """Role for users e.g. developer, trainer, user."""
    name = models.CharField(
        help_text='How would you define your participation?',
        max_length=255,
        null=False,
        blank=False,
        unique=True)
    sort_number = models.IntegerField(
        help_text='Sorting order for role in role list.',
        null=True,
        blank=True)

    def __unicode__(self):
        return self.name


class User(AbstractBaseUser):
    """User class for InaSAFE User Map."""
    name = models.CharField(
        help_text='Your name.',
        max_length=100,
        null=False,
        blank=False)
    email = models.EmailField(
        help_text='Your email.',
        null=False,
        blank=False,
        unique=True)
    website = models.URLField(
        help_text='Optional link to your personal or organisation web site.',
        null=True,
        blank=True)
    location = models.PointField(
        help_text='Where are you?',
        max_length=255,
        null=False,
        blank=False)
    role = models.ForeignKey(Role)
    email_updates = models.BooleanField(
        help_text='Tick this to receive occasional news email messages.',
        null=False,
        blank=False
    )
    is_approved = models.BooleanField(
        help_text='Whether this user has approved their entry by email.',
        null=False,
        default=False
    )
    is_active = models.BooleanField(
        help_text='Whether this user has been deleted or not.',
        default=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']


    def __unicode__(self):
        return self.name
