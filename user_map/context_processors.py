# coding=utf-8
"""Module for custom context processor for InaSAFE User Map."""
from user_map import app_settings


def user_map_settings(request):
    """Add media configuration for user map e.g favicon path so that we can
    use it directly on template.

    :param request: A django request object.
    :type request: request
    """
    return {
        'PROJECT_NAME': app_settings.PROJECT_NAME,
        'FAVICON_PATH': app_settings.FAVICON_FILE,
    }
