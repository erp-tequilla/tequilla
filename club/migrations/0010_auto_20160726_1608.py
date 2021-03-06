# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-26 12:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0009_club_formula'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='size_for_calc',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(40, '40 мл.'), (50, '50 мл.')], null=True, verbose_name='Размер мензурок (для калькулятора)'),
        ),
        migrations.AlterField(
            model_name='club',
            name='formula',
            field=models.CharField(choices=[('beaker', 'Для мензурки'), ('shot', 'Для шотов')], default='shot', max_length=10, verbose_name='Формула рассчета'),
        ),
    ]
