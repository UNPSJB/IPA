import django_tables2 as tables

from .models import Afluente, Localidad, Departamento, Establecimiento

class AfluentesTable(tables.Table):
    
    nombre = tables.Column(verbose_name="Nombre")
    localidad = tables.Column(verbose_name="Localidad")
    caudal = tables.Column(verbose_name="Caudal")
    acciones = tables.TemplateColumn(template_name="formButtons.html",orderable=False)

class LocalidadesTable(tables.Table):

    codpostal = tables.Column(verbose_name="Codigo postal")
    nombre = tables.Column(verbose_name="Nombre")
    departamento = tables.Column(verbose_name="Departamento")
    acciones = tables.TemplateColumn(template_name="formButtons.html",orderable=False)

    class Meta:
        template_name = "django_tables2/semantic.html"
        model = Localidad
        fields = ()
 
class DepartamentosTable(tables.Table):
    nombre = tables.Column(verbose_name="Nombre")
    poblacion = tables.Column(verbose_name="Poblacion")
    superficie = tables.Column(verbose_name="superficie")
    acciones = tables.TemplateColumn(template_name="formButtons.html",orderable=False)

    class Meta:
        template_name = "django_tables2/semantic.html"
        model = Departamento
        fields = ()

class EstablecimientosTable(tables.Table):
    nombre = tables.Column(verbose_name="Nombre")
    localidad = tables.Column(verbose_name="Localidad")
    codigoCatastral = tables.Column(verbose_name="Codigo Catastral")
    acciones = tables.TemplateColumn(template_name="formButtons.html",orderable=False)

    class Meta:
        template_name = "django_tables2/semantic.html"
        model = Establecimiento
        fields = ()