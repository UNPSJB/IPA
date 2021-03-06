# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-03 15:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('establecimientos', '0002_auto_20171103_1559'),
        ('personas', '0004_auto_20171020_1606'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaInicio', models.CharField(max_length=100)),
                ('fechaFin', models.CharField(max_length=100)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='establecimientos.Departamento')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personas.Persona')),
                ('localidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='establecimientos.Localidad')),
            ],
            options={
                'ordering': ['-fechaInicio'],
            },
        ),
    ]
