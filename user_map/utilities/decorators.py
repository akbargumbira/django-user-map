# coding=utf-8
"""Module that contains useful decorators."""

from django.contrib.auth.decorators import user_passes_test


def login_forbidden(function=None, redirect_to='user_map:index'):
    """Decorator for views that checks that the user is NOT logged in.

    :param function: The function parameter for this decorator.
    :type function: function

    :param redirect_to: Redirect to this URl if user_passes_test fails.
    :type redirect_to: str

    """
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated(),
        login_url=redirect_to,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

