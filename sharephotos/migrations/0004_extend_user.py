# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_last_login_null'),
        ('sharephotos', '0003_tb_tag_used_times'),
    ]

    operations = [
        migrations.CreateModel(
            name='extend_user',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('interest', models.ManyToManyField(to='sharephotos.tb_tag')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            bases=('users.user',),
        ),
    ]
