# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharephotos', '0011_tb_photo_info_store_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tb_tag',
            name='tag',
            field=models.CharField(unique=True, max_length=20),
        ),
    ]
