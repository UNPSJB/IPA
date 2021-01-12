import django_tables2 as tables
from apps.permisos.models import Permiso, TipoUso

class PermisosTable(tables.Table):
    solicitante = tables.Column(verbose_name="Solicitante")
    establecimiento = tables.Column(verbose_name="Establecimiento")
    tipo = tables.Column(verbose_name="Tipo")
    afluente = tables.Column(verbose_name="Afluente")
    estado = tables.Column(verbose_name="Estado")
    fechaSolicitud = tables.Column(verbose_name="Fecha de Solicitud")
    fechaVencimiento = tables.Column(verbose_name="Fecha de Vencimiento")
    acciones = tables.TemplateColumn(template_name="formButtons.html",orderable=False)
 
    class Meta:
        template_name = "django_tables2/semantic.html"
        model = Permiso
        fields = ()

class TipoDeUsoTable(tables.Table):
    descripcion = tables.Column(verbose_name="Nombre")
    coeficiente = tables.Column(verbose_name="Coefiente")
    periodo = tables.Column(verbose_name="Periodo")
    medida = tables.Column(verbose_name="Medida")
    tipo_modulo = tables.Column(verbose_name="Tipo de Modulo")
    acciones = tables.TemplateColumn(template_name="formButtons.html",orderable=False)