# coding=utf-8
"""Model factories definition for models."""
from django.conf import settings
from django.contrib.gis.geos import Point
import factory
from factory import DjangoModelFactory

from user_map.models import Role, UserMap


class UserFactory(DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Sequence(lambda n: 'user{0}'.format(n))


class RoleFactory(DjangoModelFactory):
    """Factory class for Role model."""
    class Meta:
        """Meta definition."""
        model = Role

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: 'Role %s' % n)
    badge = factory.Sequence(lambda n: '/path/to/badge/role%s' % n)


class UserMapFactory(DjangoModelFactory):
    """Factory class for UserMap Model"""
    class Meta:
        """"Meta definition."""
        model = UserMap

    # Taking others as default value defined in model but not these:
    name = 'John Doe'
    email = factory.Sequence(lambda n: 'john.doe%s@example.com' % n)
    password = factory.PostGenerationMethodCall(
        'set_password', 'default_password')
    location = Point(105.567, 123)
    role = factory.SubFactory(RoleFactory)
