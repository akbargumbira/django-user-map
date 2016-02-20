# coding=utf-8
"""Model factories definition for models."""
from django.contrib.gis.geos import Point
import factory
from factory import DjangoModelFactory

from user.models import Role, User


class RoleFactory(DjangoModelFactory):
    """Factory class for Role model."""
    class Meta:
        """Meta definition."""
        model = Role

    name = factory.Sequence(lambda n: 'Role %s' % n)
    sort_number = 1


class UserFactory(DjangoModelFactory):
    """Factory class for User Model"""
    class Meta:
        """"Meta definition."""
        model = User
        django_get_or_create = ('email',)

    # Taking others as default value defined in model but not these:
    name = 'John Doe'
    email = factory.Sequence(lambda n: 'john.doe%s@example.com' % n)
    password = factory.PostGenerationMethodCall(
        'set_password', 'default_password')
    location = Point(105.567, 123)
    role = factory.SubFactory(RoleFactory)
