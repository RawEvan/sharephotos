# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharephotos', '0008_tb_photo_info_store_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tb_photo_info',
            name='store_url',
            field=models.TextField(default=b'url', max_length=1250),
        ),
    ]
