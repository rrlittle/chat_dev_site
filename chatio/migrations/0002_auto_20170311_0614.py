# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-11 06:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatio', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='Message',
            new_name='message',
        ),
    ]
