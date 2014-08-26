# coding=utf-8
"""Custom User Manager for user of InaSAFE User Map."""
from django.contrib.gis.db.models import GeoManager
from django.contrib.auth.models import BaseUserManager

from user_map.models.role import Role


class CustomUserManager(BaseUserManager, GeoManager):
    """Custom user manager for user map."""
    class Meta:
        """Meta class."""
        app_label = 'user_map'

    def create_user(
            self,
            name,
            email,
            location,
            role,
            email_updates,
            website='',
            password=None):
        """Create and save a User.

        :param name: The name of the user.
        :type name: str

        :param email: The email of the user.
        :type email: str

        :param location: The location of the user in (long, lat)
        :type location: str

        :param role: The role of the user.
        :type role: Role

        :param email_updates: The status email_updates of the user.
        :type email_updates: bool

        :param website: The website of the user.
        :type website: str

        :param password: The password of the user.
        :type password: str
        """
        if not name:
            raise ValueError('User must have name.')

        if not email:
            raise ValueError('User must have an email address.')

        if not location:
            raise ValueError('User must have location.')

        if not role:
            raise ValueError('User must have role.')

        if not email_updates:
            raise ValueError('User must have email_updates status.')

        user = self.model(
            name=name,
            email=self.normalize_email(email),
            location=location,
            role=role,
            email_updates=email_updates,
            website=website
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password):
        """Create and save a superuser.

        :param name: The name of the superuser.
        :type name: str

        :param email: The email of the superuser.
        :type email: str

        :param password: The password of the superuser.
        :type password:  str
        """
        # Use predefined location, role, email_updates, is_approved, is_active,
        # is_admin
        location = 'POINT(144 5)'
        role = Role(name='Super User', sort_number=999)
        role.save()
        user = self.create_user(
            name,
            email,
            location=location,
            role=role,
            email_updates=True,
            password=password)
        user.email_updates = True
        user.is_approved = True
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user
