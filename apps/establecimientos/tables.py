import django_tables2 as tables

from .models import Afluente, Localidad

class AfluentesTable(tables.Table):
    
    nombre = tables.Column(verbose_name="Nombre")
    localidad = tables.Column(verbose_name="Localidad")
    caudal = tables.Column(verbose_name="Caudal")
    acciones = tables.TemplateColumn(template_name="formButtons.html")

class LocalidadesTable(tables.Table):

    codpostal = tables.Column(verbose_name="Codigo postal")
    nombre = tables.Column(verbose_name="Nombre")
    departamento = tables.Column(verbose_name="Departamento")

    class Meta:
        template_name = "django_tables2/semantic.html"
        model = Localidad
        fields = ()
 