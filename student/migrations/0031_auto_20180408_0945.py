# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-08 09:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0030_recent_act'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recent_act',
            name='rcatid',
        ),
        migrations.RemoveField(
            model_name='recent_act',
            name='touser',
        ),
        migrations.DeleteModel(
            name='recent_act',
        ),
    ]
