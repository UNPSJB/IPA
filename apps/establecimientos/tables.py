import django_tables2 as tables

from .models import Afluente

class AfluentesTable(tables.Table):
    
    nombre = tables.Column(verbose_name="Nombre")
    localidad = tables.Column(verbose_name="Localidad")
    caudal = tables.Column(verbose_name="Caudal")
    acciones = tables.TemplateColumn(template_name="formButtons.html")
 