# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharephotos', '0013_auto_20160109_0119'),
    ]

    operations = [
        migrations.AddField(
            model_name='tb_photo_info',
            name='owner',
            field=models.TextField(default=b'system', max_length=1250),
        ),
    ]
