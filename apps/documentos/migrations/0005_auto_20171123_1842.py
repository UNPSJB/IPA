# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-23 18:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0004_auto_20171117_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='visado',
            field=models.BooleanField(default=False),
        ),
    ]
