# coding=utf-8
"""Module related to test for all the models."""
from django.test import TransactionTestCase
from django.contrib.gis.geos import Point

from user_map.tests.model_factories import (
    RoleFactory, UserFactory, UserMapFactory)
from user_map.models.role import Role


class TestRole(TransactionTestCase):
    """Class to test Role model."""
    reset_sequences = True

    def setUp(self):
        pass

    def test_create_role(self):
        """Method to test role creation."""
        role = RoleFactory.create()
        message = 'The role is not instantiated successfully.'
        self.assertIsNotNone(role.id, message)

    def test_read_role(self):
        """Method to test reading role."""
        for i in range(3):
            RoleFactory(__sequence=i)

        for i in range(3):
            role_name = 'Role %s' % i
            role_badge = 'path/to/badge/role%s' % i

            role = Role.objects.get(pk=i)
            message = 'The role name should be %s, but it gives %s' % (
                role_name, role.name)
            self.assertEqual(role_name, role.name, message)
            message = 'The role badge should be %s, but it gives %s' % (
                role_badge, role.badge)
            self.assertEqual(role_badge, role.badge, message)

    def test_update_role(self):
        """Method to test updating role."""
        role = RoleFactory.create(name='Testing User')
        role_name = 'Updated Testing User'
        role.name = role_name
        role.save()
        message = 'The role name should be %s, but it gives %s' % (
            role_name, role.name)
        self.assertEqual(role_name, role.name, message)

    def test_delete_role(self):
        """Method to test deleting role."""
        role = RoleFactory.create()
        self.assertIsNotNone(role.id)
        role.delete()
        message = 'The role is not deleted.'
        self.assertIsNone(role.id, message)


class TestUserMap(TransactionTestCase):
    """Class to test User model."""
    def setUp(self):
        pass

    def test_create_usermap(self):
        """Method to test user map creation."""
        user_map = UserMapFactory.create()
        message = 'The user map is not instantiated successfully.'
        self.assertIsNotNone(user_map.user, message)

    def test_read_usermap(self):
        """Method to test reading user map."""
        user = UserFactory(username='John Doe')
        location = Point(5, 5)
        image = '/john/doe/image.png'

        usermap = UserMapFactory.create(
            user=user, location=location, image=image)

        message = 'The username should be %s, but it gives %s' % (
            user.username, usermap.user.username)
        self.assertEqual(user.username, usermap.user.username, message)

        message = 'The user location should be %s, but it gives %s' % (
            location, usermap.location)
        self.assertEqual(location, usermap.location, message)

        message = 'The user image should be %s, but it gives %s' % (
            image, usermap.image)
        self.assertEqual(image, usermap.image, message)

    def test_update_usermap(self):
        """Method to test updating usermap."""
        user_map = UserMapFactory()

        new_location = Point(10, 10)
        user_map.location = new_location
        user_map.save()
        message = 'The user map location should be %s, but it gives %s' % (
            new_location, user_map.location)
        self.assertEqual(new_location, user_map.location, message)

        new_image = '/new/image.png'
        user_map.image = new_image
        user_map.save()
        message = 'The user map image should be %s, but it gives %s' % (
            new_image, user_map.image)
        self.assertEqual(new_image, user_map.image, message)

    def test_delete_user(self):
        """Method to test deleting user map."""
        user_map = UserMapFactory.create()
        self.assertIsNotNone(user_map.pk)
        user_map.delete()
        message = 'The user map is not deleted.'
        self.assertIsNone(user_map.pk, message)
