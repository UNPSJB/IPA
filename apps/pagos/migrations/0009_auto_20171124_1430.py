# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-24 14:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0008_auto_20171124_0259'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cobro',
            options={'get_latest_by': 'fecha_hasta'},
        ),
        migrations.AlterField(
            model_name='pago',
            name='permiso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagos', to='permisos.Permiso'),
        ),
    ]