# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharephotos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tb_tag',
            name='used_times',
            field=models.IntegerField(default=0),
        ),
    ]
