# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('collect_time', models.DateTimeField(auto_now=True)),
                ('email', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('degree', models.IntegerField(default=0)),
                ('email', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo_url', models.TextField(default=b'url', max_length=1250)),
                ('description', models.TextField(default=b'no description', max_length=300)),
                ('upload_time', models.DateTimeField(auto_now=True)),
                ('owner', models.TextField(default=b'system', max_length=1250)),
                ('collected_times', models.IntegerField(default=0)),
                ('permission', models.CharField(default=b'private', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(unique=True, max_length=50)),
                ('is_person', models.BooleanField(default=False)),
                ('add_time', models.DateTimeField(auto_now=True)),
                ('used_times', models.IntegerField(default=1)),
            ],
        ),
        migrations.AddField(
            model_name='photo',
            name='tags',
            field=models.ManyToManyField(to='sharephotos.Tag'),
        ),
        migrations.AddField(
            model_name='interest',
            name='interested_tag',
            field=models.ForeignKey(to='sharephotos.Tag'),
        ),
        migrations.AddField(
            model_name='collect',
            name='photo_id',
            field=models.ForeignKey(to='sharephotos.Photo'),
        ),
        migrations.AlterUniqueTogether(
            name='interest',
            unique_together=set([('email', 'interested_tag')]),
        ),
        migrations.AlterUniqueTogether(
            name='collect',
            unique_together=set([('email', 'photo_id')]),
        ),
    ]
