# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-15 13:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_auto_20160615_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='discount',
            field=models.IntegerField(blank=True, null=True, verbose_name='Сумма скидки'),
        ),
        migrations.AlterField(
            model_name='report',
            name='shots_count',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, verbose_name='Количество шотов'),
        ),
        migrations.AlterField(
            model_name='report',
            name='sum_for_bar',
            field=models.IntegerField(blank=True, null=True, verbose_name='Сумма в бар'),
        ),
    ]