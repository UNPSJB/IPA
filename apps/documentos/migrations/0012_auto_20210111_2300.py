# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2021-01-11 23:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0011_auto_20171130_0441'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documento',
            name='visado',
        ),
        migrations.AddField(
            model_name='documento',
            name='estado',
            field=models.PositiveIntegerField(choices=[(0, 'Entregado'), (1, 'Rechazado'), (2, 'Visado')], default=2),
            preserve_default=False,
        ),
    ]
