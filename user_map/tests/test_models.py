# coding=utf-8
"""Module related to test for all the models."""
from django.test import TestCase

from user_map.tests.model_factories import RoleFactory, UserFactory


class TestRole(TestCase):
    """Class to test Role model."""
    def setUp(self):
        pass

    def test_create_role(self):
        """Method to test role creation."""
        role = RoleFactory.create()
        message = 'The role is not instantiated successfully.'
        self.assertIsNotNone(role.id, message)

    def test_read_role(self):
        """Method to test reading role."""
        role_name = 'Testing Role'
        role = RoleFactory.create(name=role_name)
        message = 'The role name should be %s, but it gives %s' % (
            role_name, role.name)
        self.assertEqual(role_name, role.name, message)

    def test_update_role(self):
        """Method to test updating role."""
        pass

    def test_delete_role(self):
        """Method to test deleting role."""
        pass


class TestUser(TestCase):
    """Class to test User model."""
    def setUp(self):
        pass

    def test_create_user(self):
        """Method to test user creation."""
        pass

    def test_read_user(self):
        """Method to test reading user."""
        pass

    def test_update_user(self):
        """Method to test update user."""
        pass

    def test_delete_user(self):
        """Method to test delete user."""
