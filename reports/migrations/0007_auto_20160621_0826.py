# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-21 04:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_reportdrink'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='is_filled',
        ),
        migrations.AddField(
            model_name='report',
            name='filled_date',
            field=models.DateTimeField(null=True),
        ),
    ]