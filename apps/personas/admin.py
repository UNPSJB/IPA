from django.contrib import admin
from .models import Persona, Director, Administrativo, Rol
# Register your models here.
admin.site.register(Persona)
admin.site.register(Director)
admin.site.register(Administrativo)
admin.site.register(Rol)