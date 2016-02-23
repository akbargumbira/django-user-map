# coding=utf-8
"""Module related to test for all the models."""
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from user_map.tests.model_factories import UserFactory


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
        self.assertTemplateUsed(response, 'user_map/legend.html')
        self.assertTemplateUsed(response, 'user_map/data_privacy.html')
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

    def test_show_register_page(self):
        """Test register view using get."""
        response = self.client.get(reverse('user_map:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_map/account/registration.html')

    def test_register_success(self):
        """Test register view using post."""
        response = self.client.post(
            reverse('user_map:register'),
            {
                'name': 'John Doe',
                'email': 'john.doe@gmail.com',
                'password': 'password',
                'password2': 'password',
                'website': '',
                'role': '1',
                'location': ('{"type":"Point","coordinates":[22.5,'
                             '-16.63619187839765]}')
            })
        self.assertRedirects(
            response,
            reverse('user_map:register'),
            302,
            200)

    def test_confirm_registration_invalid(self):
        """Test confirm_registration using invalid link."""
        response = self.client.get(
            reverse('user_map:confirm_registration', args=('l1nk', 'inV4lid')))
        self.assertTemplateUsed(response, 'user_map/information.html')
        self.assertContains(response, 'Your link is not valid')

    def test_confirm_registration_valid(self):
        """Test confirm_registration using valid link."""
        # Create unconfirmed user first
        user = UserFactory.create(is_confirmed=False)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        response = self.client.get(
            reverse('user_map:confirm_registration', args=(uid, user.key)))
        self.assertTemplateUsed(response, 'user_map/information.html')
        self.assertContains(
            response,
            'Congratulations! Your account has been successfully confirmed.')

    def test_show_login_page(self):
        """Test if showing login page is OK."""
        response = self.client.get(reverse('user_map:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_map/account/login.html')

    def test_login_invalid(self):
        """Test login with invalid user."""
        response = self.client.post(
            reverse('user_map:login'),
            {
                'email': 'invalid@user.com',
                'password': 'invaliduserpass'
            }
        )
        self.assertTemplateUsed(response, 'user_map/account/login.html')
        self.assertContains(
            response, 'Please enter a correct email and password')

    def test_login_valid(self):
        """Test login with valid user."""
        # Create a user first with is_confirmed = True
        UserFactory.create(
            email='test@mail.com', password='test', is_confirmed=True)

        response = self.client.post(
            reverse('user_map:login'),
            {
                'email': 'test@mail.com',
                'password': 'test'
            }
        )
        self.assertRedirects(
            response,
            reverse('user_map:index'),
            302,
            200)

    def test_logout(self):
        """Test logout view."""
        response = self.client.post(reverse('user_map:logout'))
        self.assertRedirects(
            response,
            reverse('user_map:index'),
            302,
            200)

    def test_show_update_page(self):
        """Test showing update user page view."""
        # Login first
        self.assertTrue(
            self.client.login(email=self.email, password=self.password))

        response = self.client.get(reverse('user_map:update_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_map/account/edit_user.html')

    def test_update_basic_information(self):
        """Test update basic information."""
        # Login first
        self.assertTrue(
            self.client.login(email=self.email, password=self.password))

        form_content = dict(
            {
                'name': 'UpdatedName',
                'email': self.email,
                'website': 'http://updated-site.com',
                'role': '1',
                'location': ('{"type":"Point","coordinates":[22.5, '
                             '-16.63619187839765]}'),
                'email_updates': 'on',
                'change_basic_info': 'Submit'
            }
        )
        response = self.client.post(
            reverse('user_map:update_user'), form_content)
        self.assertRedirects(
            response,
            reverse('user_map:update_user') + '#basic-information',
            302,
            200)
        user = UserFactory(email=self.email)
        self.assertEqual(user.name, form_content['name'])

    def test_change_password(self):
        """Test change password."""
        # Login first
        self.assertTrue(
            self.client.login(email=self.email, password=self.password))

        new_password = 'UpdatedPassword'
        form_content = dict(
            {
                'old_password': self.password,
                'new_password1': new_password,
                'new_password2': new_password,
                'change_password': 'Submit'
            }
        )
        response = self.client.post(
            reverse('user_map:update_user'), form_content)
        self.assertRedirects(
            response,
            reverse('user_map:update_user') + '#security',
            302,
            200)

        # Logout
        self.client.logout()

        # Login with old password will fail
        self.assertFalse(
            self.client.login(email=self.email, password=self.password))

        # Login with new password
        self.assertTrue(
            self.client.login(email=self.email, password=new_password))

    def test_delete_user(self):
        """Test delete_user view."""
        # Login first
        self.assertTrue(
            self.client.login(email=self.email, password=self.password))

        response = self.client.post(reverse('user_map:delete_user'))

        self.assertTemplateUsed(response, 'user_map/information.html')
        self.assertContains(
            response, 'You have deleted your account')

    def test_download(self):
        """Test download view."""
        response = self.client.post(reverse('user_map:download'))
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertEqual(
            response['Content-Disposition'],
            'attachment; filename="users.csv"')
        self.assertContains(response, self.user.name)
