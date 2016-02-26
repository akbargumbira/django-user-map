# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import user_map.models.user
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(help_text=b'How would you define your participation?', unique=True, max_length=100)),
                ('badge', models.CharField(help_text=b'The path to the badge', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserMap',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('location', django.contrib.gis.db.models.fields.PointField(help_text=b'Where are you?', srid=4326, max_length=255, verbose_name=b'Location')),
                ('image', models.ImageField(validators=[user_map.models.user.validate_image], upload_to=user_map.models.user.image_path, blank=True, help_text=b'Your photo', verbose_name=b'Image')),
                ('is_hidden', models.BooleanField(default=False, help_text=b'Do you wish to hide yourself on the map?', verbose_name=b'Hidden Status')),
                ('roles', models.ManyToManyField(to='user_map.Role', verbose_name=b'Roles')),
            ],
        ),
    ]
