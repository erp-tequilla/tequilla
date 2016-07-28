# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-28 12:51
from __future__ import unicode_literals

from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db import migrations


def init_permissions(apps, schema_editor):
    ExtUser = apps.get_model("extuser", "ExtUser")
    ct = ContentType.objects.get_for_model(ExtUser)

    edit_work_calendar_permission, created = Permission.objects.get_or_create(
        codename='can_edit_work_calendar', name='Редактирование расписания', content_type=ct
    )

    chief_group, created = Group.objects.get_or_create(name='chief')
    chief_group.permissions.add(edit_work_calendar_permission)

    director_group, created = Group.objects.get_or_create(name='director')
    director_group.permissions.add(edit_work_calendar_permission)


class Migration(migrations.Migration):

    dependencies = [
        ('extuser', '0019_add_permissions_for_edit_penalty'),
    ]

    operations = [
        migrations.RunPython(init_permissions),
    ]
