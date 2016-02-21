# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from user_map.app_settings import ROLES


def populate_roles(apps, schema_editor):
    """Populate roles from app setting.

    :param apps: App registry.
    :type apps: django.apps.apps

    :param schema_editor: Django db abstraction for turning model into db.
    :type schema_editor: django.db.backends.schema
    """
    Role = apps.get_model('user_map', 'Role')
    for idx, user_role in enumerate(ROLES):
        Role.objects.create(
            id=user_role['id'],
            name=user_role['name'],
            badge=user_role['badge']
        )


class Migration(migrations.Migration):

    dependencies = [
        ('user_map', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_roles)
    ]
