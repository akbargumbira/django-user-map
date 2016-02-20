# coding=utf-8
"""Module related to test for all the models."""
from django.test import TestCase

from user.tests.model_factories import RoleFactory, UserFactory


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


class TestUser(TestCase):
    """Class to test User model."""
    def setUp(self):
        pass

    def test_create_user(self):
        """Method to test user creation."""
        user = UserFactory.create()
        message = 'The user is not instantiated successfully.'
        self.assertIsNotNone(user.id, message)

        # email_updates, is_admin, is_confirmed =  False
        message = 'email_updates must be False'
        self.assertFalse(user.email_updates, message)
        message = 'is_admin must be False'
        self.assertFalse(user.is_admin, message)
        message = 'is_confirmed must be False'
        self.assertFalse(user.is_confirmed, message)

        # is_active = True
        message = 'is_active must be True'
        self.assertTrue(user.is_active, message)

    def test_read_user(self):
        """Method to test reading user."""
        user_name = 'John Doe'
        user_website = 'www.johndoe.com'
        user = UserFactory.create(name=user_name, website=user_website)
        message = 'The user name should be %s, but it gives %s' % (
            user_name, user.name)
        self.assertEqual(user_name, user.name, message)
        message = 'The user website should be %s, but it gives %s' % (
            user_website, user.website)
        self.assertEqual(user_website, user.website, message)

    def test_update_user(self):
        """Method to test update user."""
        user = UserFactory.create()
        user_name = 'Updated John Doe'
        user.name = user_name
        user.save()
        message = 'The user name should be %s, but it gives %s' % (
            user_name, user.name)
        self.assertEqual(user_name, user.name, message)

    def test_delete_user(self):
        """Method to test delete user."""
        user = UserFactory.create()
        self.assertIsNotNone(user.id)
        user.delete()
        message = 'The user is not deleted.'
        self.assertIsNone(user.id, message)
