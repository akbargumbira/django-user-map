# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from user_map.app_settings import USER_ROLES


def populate_roles(apps, schema_editor):
    """Populate roles from app setting.

    :param apps: App registry.
    :type apps: django.apps.apps

    :param schema_editor: Django db abstraction layer for turning model into db.
    :type schema_editor: django.db.backends.schema
    """
    Role = apps.get_model('user_map', 'Role')
    for idx, user_role in enumerate(USER_ROLES):
        Role.objects.create(name=user_role['name'], sort_number=(idx + 1))


class Migration(migrations.Migration):

    dependencies = [
        ('user_map', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_roles)
    ]
