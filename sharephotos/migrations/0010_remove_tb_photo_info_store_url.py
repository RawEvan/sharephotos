# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharephotos', '0009_auto_20151226_1640'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tb_photo_info',
            name='store_url',
        ),
    ]
