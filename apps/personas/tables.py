import django_tables2 as tables
from apps.personas.models import Persona
from django.utils.html import format_html

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

