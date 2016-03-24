# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharephotos', '0012_auto_20151227_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tb_tag',
            name='tag',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
