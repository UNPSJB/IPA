# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-19 20:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Liquidador',
            fields=[
                ('rol_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='personas.Rol')),
            ],
            bases=('personas.rol',),
        ),
        migrations.RenameField(
            model_name='persona',
            old_name='dirección',
            new_name='direccion',
        ),
        migrations.RenameField(
            model_name='persona',
            old_name='razónSocial',
            new_name='razonSocial',
        ),
        migrations.RenameField(
            model_name='persona',
            old_name='teléfono',
            new_name='telefono',
        ),
        migrations.RemoveField(
            model_name='rol',
            name='rolname',
        ),
        migrations.AlterField(
            model_name='rol',
            name='persona',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='personas.Persona'),
        ),
    ]
