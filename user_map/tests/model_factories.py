# coding=utf-8
"""Model factories definition for models."""
from django.contrib.gis.geos import Point
import factory
from factory import DjangoModelFactory

from user_map.models import Role, User


class RoleFactory(DjangoModelFactory):
    """Factory class for Role model."""
    class Meta:
        """Meta definition."""
        model = Role

    name = factory.Sequence(lambda n: 'Role %s' % n)
    sort_number = 1


class UserFactory(DjangoModelFactory):
    """Factory class for User MOdel"""
    class Meta:
        """"Meta definition."""
        model = User

    name = 'John Doe'
    email = factory.Sequence(lambda n: 'john.doe%s@example.com' % n)
    website = 'http://me.johndoe.com'
    location = Point(105.567, 123)
    role = factory.SubFactory(RoleFactory)
    email_updates = False
    is_approved = False
    is_active = True
    is_admin = False

