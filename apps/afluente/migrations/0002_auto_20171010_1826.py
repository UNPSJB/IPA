# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-10 18:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('afluente', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='afluente',
            options={'ordering': ['-nombre']},
        ),
    ]
