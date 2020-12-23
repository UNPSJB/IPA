import django_tables2 as tables

from .models import Comision

class ComisionTable(tables.Table):

    #localidades = tables.Column(verbose_name="localidad")
    localidades = tables.ManyToManyColumn(verbose_name="Localidades")
    empleados = tables.ManyToManyColumn(verbose_name="Empleados")
    #empleados = tables.Column(verbose_name="Empleados")
    fechaInicio = tables.Column(verbose_name="Fecha Inicio")
    fechaFin = tables.Column(verbose_name="Fecha Fin")

    class Meta:
        template_name = "django_tables2/semantic.html"
        model = Comision
        #fields = ("localidades",)