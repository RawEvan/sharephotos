# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharephotos', '0009_auto_20160503_1923'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='store_url',
            new_name='photo_url',
        ),
    ]
