# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-26 06:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0008_auto_20160630_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='formula',
            field=models.CharField(choices=[('beaker', 'Мензурка'), ('shot', 'Шот')], default='shot', max_length=10, verbose_name='Формула рассчета'),
        ),
    ]
