import django_tables2 as tables

from .models import Comision

class ComisionTable(tables.Table):

    #fechaInicio = tables.Column(verbose_name="Fecha de Inicio")
    #fechaFin = tables.Column(verbose_name="Fecha de Fin")
    id = tables.Column(verbose_name="Numero Comision",empty_values=())
    fechas = tables.Column(verbose_name="Fechas",empty_values=(),order_by=("fechaInicio","fechaFin"))
    localidades = tables.ManyToManyColumn(verbose_name="Localidades")
    empleados = tables.ManyToManyColumn(verbose_name="Empleados")
    acciones = tables.TemplateColumn(template_name="formButtons.html",orderable=False)

    class Meta:
        template_name = "django_tables2/semantic.html"
        model = Comision
        fields = ()

    def render_fechas(self,record):
        return "{} al {}".format(record.fechaInicio.strftime('%d/%m/%Y'), record.fechaFin.strftime('%d/%m/%Y'))