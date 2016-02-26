# coding=utf-8
"""Model class for Role"""
from django.contrib.gis.db import models


class Role(models.Model):
    """Role for users e.g. developer, trainer, user."""
    class Meta:
        """Meta class."""
        app_label = 'user_map'
    id = models.IntegerField(primary_key=True)
    name = models.CharField(
        help_text='How would you define your participation?',
        max_length=100,
        null=False,
        blank=False,
        unique=True)
    badge = models.CharField(
        help_text='The path to the badge',
        max_length=100,
        null=False,
        blank=False)

    def __unicode__(self):
        return self.name
