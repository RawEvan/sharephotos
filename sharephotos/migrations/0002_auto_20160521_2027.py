# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sharephotos', '0001_squashed_0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collect',
            old_name='photo_id',
            new_name='photo',
        ),
        migrations.RenameField(
            model_name='collect',
            old_name='email',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='interest',
            old_name='interested_tag',
            new_name='tag',
        ),
        migrations.RenameField(
            model_name='interest',
            old_name='email',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='photo',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='collect',
            unique_together=set([('user', 'photo')]),
        ),
        migrations.AlterUniqueTogether(
            name='interest',
            unique_together=set([('user', 'tag')]),
        ),
    ]
