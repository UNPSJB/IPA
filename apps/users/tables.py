import django_tables2 as tables
from apps.users.models import *
from django.utils.html import format_html

class UsuarioTable(tables.Table):
    username = tables.Column()
    acciones = tables.TemplateColumn(template_name="formButtons.html")

    class Meta:
        template_name = "django_tables2/semantic.html"
        model = Usuario
        fields = ()
