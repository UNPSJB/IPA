# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2020-01-13 14:40
from __future__ import unicode_literals

import apps.users.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20191005_1503'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='usuario',
            managers=[
                ('objects', apps.users.models.UsuariosManager(show_superusers=True)),
                ('usuarios', apps.users.models.UsuariosManager()),
            ],
        ),
        migrations.AlterField(
            model_name='usuario',
            name='persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personas.Persona'),
        ),
    ]
