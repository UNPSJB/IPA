# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-30 02:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0008_auto_20171129_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rol',
            name='tipo',
            field=models.PositiveSmallIntegerField(choices=[(0, 'rol'), (1, 'director'), (2, 'administrativo'), (3, 'inspector'), (8, 'jefedepartamento'), (4, 'chofer'), (5, 'solicitante'), (6, 'liquidador'), (7, 'sumariante')]),
        ),
    ]
