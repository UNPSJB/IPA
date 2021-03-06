# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-23 21:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0006_auto_20171123_0712'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cobro',
            options={'get_latest_by': 'fecha'},
        ),
        migrations.AlterModelOptions(
            name='valordemodulo',
            options={'get_latest_by': 'fecha', 'ordering': ['fecha']},
        ),
        migrations.AlterField(
            model_name='cobro',
            name='permiso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cobros', to='permisos.Permiso'),
        ),
        migrations.AlterField(
            model_name='valordemodulo',
            name='modulo',
            field=models.PositiveIntegerField(choices=[(1, 'Diesel'), (2, 'Kw')]),
        ),
    ]
