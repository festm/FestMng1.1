# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-07 14:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0024_fileupload_file_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
