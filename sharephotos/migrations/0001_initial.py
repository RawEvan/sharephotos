# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tb_photo_info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('store_url', models.CharField(unique=True, max_length=100)),
                ('description', models.TextField(default=b'no description', max_length=300)),
                ('upload_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='tb_tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(unique=True, max_length=10)),
                ('is_face', models.BooleanField(default=False)),
                ('add_time', models.DateTimeField(auto_now=True)),
                ('photo', models.ManyToManyField(to='sharephotos.tb_photo_info')),
            ],
        ),
    ]
