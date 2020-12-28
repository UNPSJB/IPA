import django_tables2 as tables


class TipoDocumentosTable(tables.Table):
    
    nombre = tables.Column(verbose_name="Nombre")
    acciones = tables.TemplateColumn(template_name="formButtons.html",orderable=False)