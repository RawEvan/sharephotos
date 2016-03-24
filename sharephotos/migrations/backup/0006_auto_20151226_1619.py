# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharephotos', '0005_auto_20151226_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tb_photo_info',
            name='store_url',
            field=models.TextField(max_length=1250),
        ),
    ]
