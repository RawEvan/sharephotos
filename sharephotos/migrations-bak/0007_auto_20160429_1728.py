# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharephotos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='interest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=255)),
                ('interested_tag', models.CharField(max_length=50)),
                ('degree', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='interest',
            unique_together=set([('email', 'interested_tag')]),
        ),
    ]
