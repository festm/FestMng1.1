# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-07 12:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0021_merge_20180407_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='result',
            field=models.CharField(default='notseen', max_length=255),
        ),
    ]
