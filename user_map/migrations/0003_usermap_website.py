# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_map', '0002_populate_roles'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermap',
            name='website',
            field=models.URLField(help_text=b'Optional link to your personal or organisation web site', verbose_name=b'Website', blank=True),
        ),
    ]
