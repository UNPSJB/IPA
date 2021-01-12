import django_tables2 as tables

from .models import Comision

class ComisionTable(tables.Table):

    localidades = tables.ManyToManyColumn(verbose_name="Localidades")
    empleados = tables.ManyToManyColumn(verbose_name="Empleados")
    fechaInicio = tables.Column(verbose_name="Fecha Inicio")
    fechaFin = tables.Column(verbose_name="Fecha Fin")
    acciones = tables.TemplateColumn(template_name="formButtons.html",orderable=False)

    class Meta:
        template_name = "django_tables2/semantic.html"
        model = Comision