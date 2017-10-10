# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 20:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tiposDocumentacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoUso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('coeficiente', models.IntegerField()),
                ('periodo', models.CharField(choices=[('0', 'unidad'), ('1', 'm'), ('2', 'm2'), ('3', 'm3'), ('4', 'Ha'), ('5', 'KW')], max_length=1)),
                ('medida', models.CharField(choices=[('0', 'hora'), ('1', 'dia'), ('2', 'mes'), ('3', 'año')], max_length=1)),
                ('documentos', models.ManyToManyField(to='tiposDocumentacion.TipoDocumentacion')),
            ],
        ),
    ]