# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-29 09:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0004_auto_20160629_1338'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='menu',
            name='order',
            field=models.SmallIntegerField(default=0, verbose_name='Сортировка'),
        ),
    ]
