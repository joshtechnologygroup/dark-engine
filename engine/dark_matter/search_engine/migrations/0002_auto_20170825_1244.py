# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 12:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_engine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entityscore',
            name='score',
            field=models.FloatField(),
        ),
    ]
