# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-11 11:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_poll_users_watched_results'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='def_answer',
        ),
    ]
