# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-22 23:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0004_valordemodulo_modulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valordemodulo',
            name='modulo',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='valordemodulo',
            unique_together=set([('fecha', 'modulo')]),
        ),
    ]
