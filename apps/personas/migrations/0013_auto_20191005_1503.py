# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-10-05 15:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0012_auto_20190915_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='numeroDocumento',
            field=models.CharField(max_length=13, unique=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='tipoDocumento',
            field=models.CharField(choices=[('1', 'DNI'), ('2', 'LC'), ('3', 'LE'), ('4', 'PASS'), ('5', 'CUIL')], max_length=1),
        ),
    ]