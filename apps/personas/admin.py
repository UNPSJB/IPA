from django.contrib import admin
from .models import Persona, Director, Administrativo, Rol, Inspector, Sumariante, JefeDepartamento, Liquidador, Chofer, Solicitante
# Register your models here.
admin.site.register(Persona)
admin.site.register(Director)
admin.site.register(Administrativo)
admin.site.register(Inspector)
admin.site.register(Sumariante)
admin.site.register(JefeDepartamento)
admin.site.register(Liquidador)
admin.site.register(Chofer)
admin.site.register(Solicitante)
admin.site.register(Rol)