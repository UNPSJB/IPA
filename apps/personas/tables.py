import django_tables2 as tables
from apps.personas.models import *
from django.utils.html import format_html
import django_filters

def get_roles_choices():
    choices = []
    for rol in Persona.tipoRol:
        evaluado = eval(rol)
        choices.append((evaluado.TIPO, evaluado.roleName))
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
    roles = django_filters.ChoiceFilter(choices=get_roles_choices())

   