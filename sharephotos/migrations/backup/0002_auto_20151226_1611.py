# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharephotos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tb_photo_info',
            name='store_url',
            field=models.TextField(unique=True, max_length=1000),
        ),
    ]
