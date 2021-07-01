# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2021-01-15 04:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permisos', '0016_auto_20210111_2343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otorgado',
            name='monto',
        ),
        migrations.AddField(
            model_name='otorgado',
            name='fecha_vencimiento',
            field=models.DateField(),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='estado',
            name='tipo',
            field=models.PositiveSmallIntegerField(choices=[(0, 'estado'), (1, 'solicitado'), (2, 'corregido'), (3, 'visado'), (4, 'completado'), (5, 'publicado'), (6, 'otorgado'), (7, 'baja')]),
        ),
    ]