from django.contrib import admin

# Register your models here.
from .models import TipoDocumento, Documento
# Register your models here.
admin.site.register(TipoDocumento)
admin.site.register(Documento)