# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-08 01:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0026_merge_20180407_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='callmeet',
            name='stat',
            field=models.CharField(default='not seen', max_length=256),
        ),
    ]
