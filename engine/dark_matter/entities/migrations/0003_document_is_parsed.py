# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 16:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0002_auto_20170825_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='is_parsed',
            field=models.BooleanField(default=False),
        ),
    ]
