# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-07 20:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0023_callmeet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callmeet',
            name='rep',
            field=models.CharField(default='blah', max_length=256),
        ),
    ]
