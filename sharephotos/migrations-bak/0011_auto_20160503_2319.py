# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharephotos', '0010_auto_20160503_2241'),
    ]

    operations = [
        migrations.AddField(
            model_name='collect',
            name='photo_id',
            field=models.IntegerField(default=0, max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='collect',
            unique_together=set([('email', 'photo_id')]),
        ),
        migrations.RemoveField(
            model_name='collect',
            name='photo_url',
        ),
    ]
