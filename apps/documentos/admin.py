from django.contrib import admin

# Register your models here.
from .models import TipoDocumento, Documento

class TipoDocumentoAdmin(admin.ModelAdmin):
	repopulated_fields = {"slug": ("nombre",)}
	exclude = ('protegido', )

# Register your models here.
admin.site.register(TipoDocumento, TipoDocumentoAdmin)
admin.site.register(Documento)