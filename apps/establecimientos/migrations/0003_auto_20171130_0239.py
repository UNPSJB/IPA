# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-30 02:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('establecimientos', '0002_auto_20171103_1559'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='localidad',
            options={'ordering': ['nombre']},
        ),
        migrations.AlterField(
            model_name='departamento',
            name='nombre',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='localidad',
            name='codpostal',
            field=models.IntegerField(unique=True),
        ),
    ]
