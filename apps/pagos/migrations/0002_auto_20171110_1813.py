# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-10 21:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrarvalordemodulo',
            name='modulo',
        ),
        migrations.DeleteModel(
            name='Modulo',
        ),
    ]
