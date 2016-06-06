# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharephotos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Similarity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('similar_count', models.IntegerField(default=0)),
                ('similar_degree', models.FloatField(default=0.0)),
                ('photo_1', models.ForeignKey(related_name='photo_1', to='sharephotos.Photo')),
                ('photo_2', models.ForeignKey(related_name='photo_2', to='sharephotos.Photo')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='similarity',
            unique_together=set([('photo_1', 'photo_2')]),
        ),
    ]
