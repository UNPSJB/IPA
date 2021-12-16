import django_tables2 as tables
from apps.users.models import *
from django.utils.html import format_html


class UsuarioTable(tables.Table):
    username = tables.Column()
    persona = tables.Column(verbose_name="Persona")
    email = tables.Column(verbose_name="Email")
    acciones = tables.TemplateColumn(template_name="formButtons.html",orderable=False,attrs={"th": {"id": "acciones"}})

    class Meta:
        template_name = "django_tables2/semantic.html"
        model = Usuario
        fields = ()
    
    def render_persona(self,record):
        return "{}".format(record.persona)
    
    def render_email(self,record):
        return "{}".format(record.email)