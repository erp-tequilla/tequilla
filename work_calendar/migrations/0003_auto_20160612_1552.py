# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-12 11:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('work_calendar', '0002_auto_20160611_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshift',
            name='special_config',
            field=models.CharField(choices=[('cant_work', 'Не работаем'), ('trainee', 'Стажер'), ('employee', 'Сотрудник')], default='employee', max_length=12, verbose_name='Кто работает'),
        ),
        migrations.AlterField(
            model_name='workshift',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник'),
        ),
    ]
