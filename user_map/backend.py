# coding=utf-8
from django.conf import settings
from django.contrib.auth.models import check_password
from user_map.models import User


class EmailAuthBackend(object):
    """A custom authentication backend.

    Allows users to log in using their email address.
    """

    def authenticate(self, email=None, password=None):
        """Authentication method.

        :param email: The email of the user.
        :type email: str

        :param password: The password of the user.
        :type password: str

        :return: The user object if it is authenticated successfully.
        """
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """Get user based on the id.

        :param user_id: The id of the user record.
        :type user_id: str

        :return: The user object if exist, otherwise None.
        """
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None
