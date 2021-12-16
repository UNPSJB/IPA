import django_tables2 as tables
from apps.permisos.models import Permiso, TipoUso

class PermisosTable(tables.Table):
    numero_exp = tables.Column(verbose_name="Expediente/Número",empty_values=())
    solicitante = tables.Column(verbose_name="Solicitante")
    establecimiento = tables.Column(verbose_name="Establecimiento")
    tipo = tables.Column(verbose_name="Tipo")
    estado = tables.Column(verbose_name="Estado",orderable=False)
    fechaSolicitud = tables.Column(verbose_name="Fecha de Solicitud")
    fechaVencimiento = tables.Column(verbose_name="Fecha de Vencimiento")
    acciones = tables.TemplateColumn(template_name="formButtons.html",orderable=False)
 
    class Meta:
        template_name = "django_tables2/semantic.html"
        model = Permiso
        fields = ()

    def render_numero_exp(self,record):
        if record.numero_exp == None:
            return record.pk
        else:
            return record.numero_exp

class TipoDeUsoTable(tables.Table):
    descripcion = tables.Column(verbose_name="Nombre")
    coeficiente = tables.Column(verbose_name="Coefiente")
    periodo = tables.Column(verbose_name="Periodo")
    medida = tables.Column(verbose_name="Medida")
    tipo_modulo = tables.Column(verbose_name="Tipo de Módulo")
    acciones = tables.TemplateColumn(template_name="formButtons.html",orderable=False)