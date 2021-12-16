from django.db.models import fields
import django_tables2 as tables
from apps.personas.models import *
from django.utils.html import format_html
import django_filters


class PersonaTable(tables.Table):
    nombre = tables.Column()
    tipoDocumento = tables.Column(verbose_name="Tipo de Documento")
    numeroDocumento = tables.Column(verbose_name="Número de Documento")
    acciones = tables.TemplateColumn(template_name="formButtons.html",orderable=False,attrs={"th": {"id": "acciones"}})
    
    def render_nombre(self, value, record):
        return format_html("{} {}", value, record.apellido)

    class Meta:
        template_name = "django_tables2/semantic.html"
        model = Persona
        fields = ()

class EmpresaTable(tables.Table):
    razonSocial = tables.Column(verbose_name="Razón Social")
    cuit = tables.Column(verbose_name="Cuit")
    acciones = tables.TemplateColumn(template_name="formButtons.html",orderable=False,attrs={"th": {"id": "acciones"}})

class EmpresaFilter(django_filters.FilterSet):
    razonSocial = django_filters.CharFilter(label='Razón Social', lookup_expr='icontains')
    cuit = django_filters.CharFilter(label='Cuit', lookup_expr='icontains')

    class Meta:
        model = Persona
        fields = ['razonSocial','cuit']
    
   