# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2021-01-11 23:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0012_auto_20210111_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='estado',
            field=models.PositiveIntegerField(choices=[(0, 'Entregado'), (1, 'Rechazado'), (2, 'Visado')], default=0),
        ),
    ]
