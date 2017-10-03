# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 20:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('establecimientos', '0001_initial'),
        ('personas', '0001_initial'),
        ('tiposDeUso', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_solicitud', models.DateField()),
                ('utilizando', models.BooleanField()),
                ('establecimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='establecimientos.Establecimiento')),
                ('solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personas.Persona')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tiposDeUso.TipoUso')),
            ],
        ),
    ]
