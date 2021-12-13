from django.db.models import fields
import django_tables2 as tables
from apps.personas.models import *
from django.utils.html import format_html
import django_filters

def get_roles_choices():
    choices = []
    for rol in Persona.tipoRol:
        evaluado = eval(rol)
        choices.append((evaluado.TIPO, rol))
    return choices


class PersonaTable(tables.Table):
    nombre = tables.Column()
    tipoDocumento = tables.Column(verbose_name="Tipo de Documento")
    numeroDocumento = tables.Column(verbose_name="Número de Documento")
    acciones = tables.TemplateColumn(template_name="formButtons.html")
    
    def render_nombre(self, value, record):
        return format_html("{} {}", value, record.apellido)

    class Meta:
        template_name = "django_tables2/semantic.html"
        model = Persona
        fields = ()

class PersonaFilter(django_filters.FilterSet):
    roles__tipo = django_filters.ChoiceFilter(choices=get_roles_choices())

    class Meta:
        model = Persona
        fields = ['roles__tipo']

class EmpresaTable(tables.Table):
    razonSocial = tables.Column(verbose_name="Razón Social")
    cuit = tables.Column(verbose_name="Cuit")
    acciones = tables.TemplateColumn(template_name="formButtons.html")

class EmpresaFilter(django_filters.FilterSet):
    razonSocial = django_filters.CharFilter(label='Razon Social', lookup_expr='icontains')
    cuit = django_filters.CharFilter(label='Cuit', lookup_expr='icontains')

    class Meta:
        model = Persona
        fields = ['razonSocial','cuit']
    
   