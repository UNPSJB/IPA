from django.contrib import admin

from .models import Permiso, TipoUso, Estado, Solicitado
# Register your models here.
admin.site.register(Permiso)
admin.site.register(TipoUso)
admin.site.register(Estado)
admin.site.register(Solicitado)
