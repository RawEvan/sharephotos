# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharephotos', '0008_auto_20160503_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=255)),
                ('photo_url', models.TextField(default=b'url', max_length=1250)),
                ('Collect_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='tb_photo',
            new_name='Photo',
        ),
        migrations.RenameModel(
            old_name='tb_tag',
            new_name='Tag',
        ),
        migrations.AlterUniqueTogether(
            name='collect',
            unique_together=set([('email', 'photo_url')]),
        ),
    ]
