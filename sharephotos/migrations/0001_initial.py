# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tb_photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('store_url', models.TextField(default=b'url', max_length=1250)),
                ('description', models.TextField(default=b'no description', max_length=300)),
                ('upload_time', models.DateTimeField(auto_now=True)),
                ('owner', models.TextField(default=b'system', max_length=1250)),
                ('collected_times', models.IntegerField(default=0)),
                ('permission', models.CharField(default=b'private', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='tb_tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(unique=True, max_length=50)),
                ('is_face', models.BooleanField(default=False)),
                ('add_time', models.DateTimeField(auto_now=True)),
                ('used_times', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='tb_photo',
            name='tags',
            field=models.ManyToManyField(to='sharephotos.tb_tag'),
        ),
    ]
