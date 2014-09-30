# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('name', models.CharField(help_text=b'Your name.', max_length=100, verbose_name=b'Name')),
                ('email', models.EmailField(help_text=b'Your email.', unique=True, max_length=75, verbose_name=b'E-mail')),
                ('website', models.URLField(help_text=b'Optional link to your personal or organisation web site.', verbose_name=b'Website', blank=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(help_text=b'Where are you?', srid=4326, max_length=255, verbose_name=b'Location')),
                ('email_updates', models.BooleanField(default=False, help_text=b'Tick this to receive occasional news email messages.', verbose_name=b'Receiving Updates')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name=b'Join Date')),
                ('is_active', models.BooleanField(default=True, help_text=b'Whether this user is still active or not (a user could be banned or deleted).', verbose_name=b'Active Status')),
                ('is_admin', models.BooleanField(default=False, help_text=b'Whether this user is admin or not.', verbose_name=b'Admin Status')),
                ('is_confirmed', models.BooleanField(default=False, help_text=b'Whether this user has approved their entry by email.', verbose_name=b'Confirmation Status')),
                ('key', models.CharField(help_text=b'Confirmation key for user to activate their account.', max_length=40, verbose_name=b'Confirmation Key')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'How would you define your participation?', unique=True, max_length=100)),
                ('sort_number', models.IntegerField(help_text=b'Sorting order for role in role list.', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(verbose_name=b'Role', to='user_map.Role'),
            preserve_default=True,
        ),
    ]
