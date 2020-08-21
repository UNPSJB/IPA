import django_tables2 as tables
from apps.permisos.models import Permiso
class PermisosTable(tables.Table):
    solicitante = tables.Column(verbose_name="Solicitante")
    establecimiento = tables.Column(verbose_name="Establecimiento")
    tipo = tables.Column(verbose_name="Tipo")
    afluente = tables.Column(verbose_name="Afluente")
    estado = tables.Column(verbose_name="Estado")
    fechaSolicitud = tables.Column(verbose_name="Fecha de Solicitud")
    fechaVencimiento = tables.Column(verbose_name="Fecha de Vencimiento")
    acciones = tables.TemplateColumn(template_name="formButtons.html")
 
    class Meta:
        template_name = "django_tables2/semantic.html"
        model = Permiso
        fields = ()