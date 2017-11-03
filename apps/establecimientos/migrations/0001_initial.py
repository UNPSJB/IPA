# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 20:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Establecimiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigoCatastral', models.CharField(max_length=100)),
                ('superficie', models.IntegerField()),
                ('nombre', models.CharField(max_length=50)),
                ('descripción', models.CharField(max_length=100)),
                ('duenio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personas.Persona')),
            ],
        ),
    ]
