from django.contrib import admin
from .models import Persona, Director, Administrativo
# Register your models here.
admin.site.register(Persona)
admin.site.register(Director)
admin.site.register(Administrativo)