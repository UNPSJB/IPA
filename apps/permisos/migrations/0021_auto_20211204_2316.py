# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2021-12-04 23:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('permisos', '0020_auto_20211118_1058'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='permiso',
            options={'permissions': (('listar_permiso', 'Listar permisos'), ('cargar_permiso', 'Cargar permisos'), ('modificar_permiso', 'Modificar permisos'), ('eliminar_permiso', 'Eliminar permisos'), ('detalle_permiso', 'Ver detalle de permisos'), ('listar_documentacion_presentada', 'Listar documentación presentada'), ('visar_documentacion_solicitud', 'Visar documentacion de solicitud'), ('rechazar_documentacion_solicitud', 'Rechazar documentación de solicitud'))},
        ),
        migrations.AlterModelOptions(
            name='tipouso',
            options={'permissions': (('cargar_tipo_de_uso', 'Cargar tipos de usos'), ('detalle_tipo_de_uso', 'Ver detalle de tipos de usos'), ('listar_tipo_de_uso', 'Listar tipos de usos'), ('eliminar_tipo_de_uso', 'Eliminar tipos de usos'), ('modificar_tipo_de_uso', 'Modificar tipos de usos'))},
        ),
    ]
