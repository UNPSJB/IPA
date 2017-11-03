# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 19:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personas', '0004_auto_20171020_1606'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reclamo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lugar', models.CharField(max_length=100)),
                ('fecha', models.DateField(max_length=100)),
                ('motivo', models.TextField()),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personas.Persona')),
            ],
            options={
                'ordering': ['-persona'],
            },
        ),
    ]
