# coding=utf-8
"""Model class of custom user for InaSAFE User Map."""
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.gis.db import models
from django.utils.crypto import get_random_string

from user_map.models.user_manager import CustomUserManager
from user_map.models.role import Role


class User(AbstractBaseUser):
    """User class for InaSAFE User Map."""
    class Meta:
        """Meta class."""
        app_label = 'user_map'

    name = models.CharField(
        verbose_name='Name',
        help_text='Your name.',
        max_length=100,
        null=False,
        blank=False)
    email = models.EmailField(
        verbose_name='E-mail',
        help_text='Your email.',
        null=False,
        blank=False,
        unique=True)
    website = models.URLField(
        verbose_name='Website',
        help_text='Optional link to your personal or organisation web site.',
        null=False,
        blank=True)
    location = models.PointField(
        verbose_name='Location',
        help_text='Where are you?',
        max_length=255,
        null=False,
        blank=False)
    role = models.ForeignKey(Role, verbose_name='Role', blank=False)
    email_updates = models.BooleanField(
        verbose_name='Receiving Updates',
        help_text='Tick this to receive occasional news email messages.',
        default=False)
    date_joined = models.DateTimeField(
        verbose_name='Join Date',
        auto_now_add=True)
    is_active = models.BooleanField(
        verbose_name='Active Status',
        help_text='Whether this user is still active or not (a user could be '
                  'banned or deleted).',
        default=True)
    is_admin = models.BooleanField(
        verbose_name='Admin Status',
        help_text='Whether this user is admin or not.',
        default=False)
    is_confirmed = models.BooleanField(
        verbose_name='Confirmation Status',
        help_text='Whether this user has approved their entry by email.',
        null=False,
        default=False)
    key = models.CharField(
        verbose_name='Confirmation Key',
        help_text='Confirmation key for user to activate their account.',
        max_length=40)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __unicode__(self):
        return self.name

    def get_full_name(self):
        """ A longer formal identifier of the user.

        :return: The full name of a user.
        :rtype: str
        """
        return self.name

    def get_short_name(self):
        """ A shorter formal identifier of the user.

        :return: The full name of a user.
        :rtype: str
        """
        return self.name

    @property
    def is_staff(self):
        """The staff status of a user.

        Staff is determined by the admin status of a user.

        :return: True if the user is an admin, otherwise False.
        :rtype: bool
        """
        return self.is_admin

    # noinspection PyUnusedLocal
    def has_perm(self, perm, obj=None):
        """Returns true if the user has the named permission.

        :param perm: The permission.
        :type perm: str

        :param obj: The object that will be used to check the permission.
        :type obj: object

        :return: The permission status.
        :rtype: bool
        """
        return self.is_admin

    # noinspection PyUnusedLocal
    def has_module_perms(self, app_label):
        """Returns True if the user has permission to access models of the app.

        :param app_label: The application.
        :type app_label: str

        :return: The permission status.
        :rtype: bool
        """
        return self.is_admin

    def save(self, *args, **kwargs):
        """Override save method."""
        if not self.pk:
            # New object here
            self.key = get_random_string()
        super(User, self).save()
