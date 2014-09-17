# coding=utf-8
"""Module related to test for all the models."""
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from user_map.tests.model_factories import UserFactory, RoleFactory


class UserMapViewTests(TestCase):
    """Class for testing user map view."""
    def setUp(self):
        """Run for each test."""
        self.email = 'test@gmail.com'
        self.password = 'test'
        self.user = UserFactory.create(
            email=self.email,
            password=self.password,
            role__name='Test User',
            is_confirmed=True)
        self.client = Client()

    def test_index(self):
        """Test for index view."""
        response = self.client.get(reverse('user_map:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Legend')
        self.assertContains(response, 'Data Privacy')
        self.assertContains(response, 'Sign Up')
        self.assertContains(response, 'Log In')

    def test_index_login(self):
        """Test for index view after logging in."""
        self.assertTrue(
            self.client.login(email=self.email, password=self.password))
        response = self.client.get(reverse('user_map:index'))
        self.assertNotContains(response, 'Sign Up')
        self.assertNotContains(response, 'Log In')
        self.assertContains(response, 'Hi, %s' % self.user.name)

    def test_get_users(self):
        """Test for get_users view."""
        response = self.client.get(
            reverse('user_map:get_users'),
            {'user_role': 'Test User'})
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertContains(response, 'FeatureCollection')
        self.assertContains(response, self.user.name)

    def test_get_users_with_post(self):
        """Test get_users view."""
        response = self.client.post(
            reverse('user_map:get_users'),
            {'user_role': 'Test User'})
        self.assertEqual(response.status_code, 404)
