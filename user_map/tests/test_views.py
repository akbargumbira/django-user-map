# coding=utf-8
"""Module related to test for all the models."""
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.gis.geos import Point

from user_map.tests.model_factories import UserFactory, UserMapFactory
from user_map.app_settings import LOGIN_VIEW
from user_map.models import UserMap


class UserMapViewTests(TestCase):
    """Class for testing user map view."""
    def setUp(self):
        """Run for each test."""
        self.not_mapped_username = 'test@gmail.com'
        self.not_mapped_password = 'test'
        self.not_mapped_user = UserFactory.create(
            username=self.not_mapped_username,
            password=self.not_mapped_password)

        self.mapped_username = 'test2@gmail.com'
        self.mapped_password = 'test2'
        self.mapped_user = UserFactory.create(
            username=self.mapped_username,
            password=self.mapped_password)
        self.mapped_user_map = UserMapFactory(user=self.mapped_user)

        self.client = Client()

    def test_index(self):
        """Test for index view."""
        response = self.client.get(reverse('user_map:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_map/data_privacy.html')
        self.assertTemplateUsed(response, 'user_map/index.html')

    def test_index_login_mapped(self):
        """Test for index view after logging in for mapped user."""
        self.assertTrue(
            self.client.login(
                username=self.mapped_username,
                password=self.mapped_password))
        response = self.client.get(reverse('user_map:index'))
        self.assertNotContains(response, 'user-menu-add-button')
        self.assertContains(response, 'user-menu-edit-button')

    def test_list_users(self):
        """Test for listing all the users through REST API."""
        response = self.client.get(reverse('user_map:usermap-list'))
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertContains(response, 'FeatureCollection')
        self.assertContains(response, self.mapped_user.username)

    def test_list_users_with_post(self):
        """Test list user view."""
        response = self.client.post(reverse('user_map:usermap-list'))
        self.assertEqual(response.status_code, 405)  # 405 = not allowed

    def test_add_user_page_without_login(self):
        """Test showing 'add user' page without log in first.

        Should redirect to index page"""
        response = self.client.get(reverse('user_map:add'))
        self.assertRedirects(
            response,
            reverse(LOGIN_VIEW) + '?next=' + reverse('user_map:add'),
            302,
            200)

    def test_add_user_page_with_unmapped_user(self):
        """Test showing 'add user' view using get."""
        # login with unmapped user
        self.assertTrue(
            self.client.login(
                username=self.not_mapped_username,
                password=self.not_mapped_password))
        response = self.client.get(reverse('user_map:add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_map/user_add_update.html')

    def test_add_user_page_with_mapped_user(self):
        """Test accessing 'add user page' with mapped user.

        Should redirect to index page.
        """
        # login with mapped user
        self.assertTrue(
            self.client.login(
                username=self.mapped_username,
                password=self.mapped_password))
        response = self.client.get(reverse('user_map:add'))
        self.assertRedirects(
            response,
            reverse('user_map:index'),
            302,
            200)

    def test_add_user_success(self):
        """Test adding user map using post."""
        # login with unmapped user
        self.assertTrue(
            self.client.login(
                username=self.not_mapped_username,
                password=self.not_mapped_password))
        response = self.client.post(
            reverse('user_map:add'),
            {
                'roles': '1',
                'location': ('{"type":"Point","coordinates":[22.5,'
                             '-16.63619187839765]}'),
                'image': '',
                'csrfmiddlewaretoken': u'yxeoT16pTxofWArnbgfAOudInBqAOpyq'
            })
        self.assertRedirects(
            response,
            reverse('user_map:index'),
            302,
            200)

    def test_show_update_page(self):
        """Test showing update user page view."""
        # Login first with mapped user
        self.assertTrue(
            self.client.login(
                username=self.mapped_username,
                password=self.mapped_password))

        response = self.client.get(reverse('user_map:update'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_map/user_add_update.html')

    def test_update_user(self):
        """Test update user."""
        # Login first with mapped user
        self.assertTrue(
            self.client.login(
                username=self.mapped_username,
                password=self.mapped_password))

        form_content = dict(
            {
                'roles': '1',
                'location': ('{"type":"Point","coordinates":[22.5,'
                             '-16.63619187839765]}'),
                # 'image': 'john/doe/cool.png',
                'csrfmiddlewaretoken': u'yxeoT16pTxofWArnbgfAOudInBqAOpyq'
            }
        )
        response = self.client.post(
            reverse('user_map:update'), form_content)
        self.assertRedirects(
            response,
            reverse('user_map:index'),
            302,
            200)
        user_map = UserMap.objects.get(user=self.mapped_user)
        new_point = Point(22.5, -16.63619187839765)
        self.assertAlmostEqual(user_map.location.x, new_point.x)
        self.assertAlmostEqual(user_map.location.y, new_point.y)
