# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-27 02:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permisos', '0012_permiso_fechasolicitud'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permiso',
            name='fechaSolicitud',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
    ]
