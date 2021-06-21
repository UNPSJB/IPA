import django_tables2 as tables

from django.db.models import F

from .models import Cobro, Pago, ValorDeModulo

def DocumentColumn(tipo):
    return tables.TemplateColumn('<div><a href="/archivos/{{record.documento.archivo.url}}" class="ui icon">{{record.documento.descripcion}}</a></div>',
                                verbose_name="Documento de "+tipo,
                                orderable=False                               
    )

class CobrosTable(tables.Table):
    periodo = tables.Column(empty_values=(),order_by=("fecha_desde","fecha_hasta"))
    fecha = tables.DateColumn(short=False,verbose_name="Fecha de Cobro", attrs={"td": {"id": lambda record: "fecha-"+str(record.id)}})
    monto = tables.Column(verbose_name="Monto ($)", attrs={"td": {"id": lambda record: "monto-"+str(record.id)}})
    es_por_canon = tables.BooleanColumn(verbose_name="Tipo",yesno="Canon,Infraccion", attrs={"td": {"id": lambda record: "tipo-"+str(record.id)}})
    documentocob = DocumentColumn("Cobro")
    acciones = tables.TemplateColumn(verbose_name="Acciones", template_name="formButtons.html", orderable=False)
    
    class Meta:
        template_name = "django_tables2/semantic.html"
        model = Cobro
        fields = ()
        row_attrs = {
            "id": lambda record: "cobro-"+str(record.id)
        }

    def render_periodo(self,record):
        return "{} al {}".format(record.fecha_desde.strftime('%d/%m/%Y'), record.fecha.strftime('%d/%m/%Y'))

class CobrosTodosTable(tables.Table):
    solicitante = tables.Column(verbose_name="Solicitante",accessor="permiso.solicitante")
    tipo = tables.Column(verbose_name="Tipo de Permiso",accessor="permiso.tipo")
    periodo = tables.Column(empty_values=(),order_by=("fecha_desde","fecha_hasta"))
    fecha = tables.DateColumn(short=False,verbose_name="Fecha de Cobro")
    monto = tables.Column(verbose_name="Monto($)")
    documentocob = DocumentColumn("Cobro")
    es_por_canon = tables.BooleanColumn(verbose_name="Tipo de Cobro",yesno="Canon,Infraccion")
    
    class Meta:
        template_name = "django_tables2/semantic.html"
        model = Cobro
        fields = ()

    def render_periodo(self,record):
        return "{} al {}".format(record.fecha_desde.strftime('%d/%m/%Y'), record.fecha.strftime('%d/%m/%Y'))


class PagosTable(tables.Table):
    fecha = tables.DateColumn(short=False,verbose_name="Fecha de Pago", attrs={"td": {"id": lambda record: "fecha-"+str(record.id)}})
    monto = tables.Column(verbose_name="Monto ($)", attrs={"td": {"id": lambda record: "monto-"+str(record.id)}})
    es_por_canon = tables.BooleanColumn(verbose_name="Tipo",yesno="Canon,Infraccion", attrs={"td": {"id": lambda record: "tipo-"+str(record.id)}})
    documento = DocumentColumn("Pago")
    acciones = tables.TemplateColumn(verbose_name="Acciones", template_name="formButtons.html", orderable=False)

    class Meta:
        template_name = "django_tables2/semantic.html"
        model = Pago
        fields = ()
        row_attrs = {
            "id": lambda record: "pago-"+str(record.id)
        }

class PagosTodosTable(tables.Table):
    solicitante = tables.Column(verbose_name="Solicitante",accessor="permiso.solicitante")
    tipo = tables.Column(verbose_name="Tipo de Permiso",accessor="permiso.tipo")
    fecha = tables.DateColumn(short=False,verbose_name="Fecha de Pago")
    monto = tables.Column(verbose_name="Monto($)")
    documentocob = DocumentColumn("Pago")
    es_por_canon = tables.BooleanColumn(verbose_name="Tipo de Pago",yesno="Canon,Infraccion")


class ModulosTable(tables.Table):
    precio = tables.Column(verbose_name="Precio($)")
    fecha = tables.DateColumn(verbose_name="Fecha")
    modulo = tables.Column(verbose_name="Tipo")
    descripcion = tables.Column(verbose_name="Descripción")
    acciones = tables.TemplateColumn(verbose_name="Acciones", template_name="formButtons.html", orderable=False)

    class Meta:
        template_name = "django_tables2/semantic.html"
        model = ValorDeModulo
        fields = ()