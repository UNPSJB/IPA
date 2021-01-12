# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2021-01-11 23:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('permisos', '0015_auto_20200904_2136'),
    ]

    operations = [
        migrations.CreateModel(
            name='Corregido',
            fields=[
                ('estado_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='permisos.Estado')),
                ('fecha_corregido', models.DateField()),
            ],
            bases=('permisos.estado',),
        ),
        migrations.AlterField(
            model_name='estado',
            name='tipo',
            field=models.PositiveSmallIntegerField(choices=[(0, 'estado'), (1, 'solicitado'), (3, 'visado'), (4, 'completado'), (5, 'publicado'), (6, 'otorgado'), (7, 'baja')]),
        ),
    ]
