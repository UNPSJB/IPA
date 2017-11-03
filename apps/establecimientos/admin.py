from django.contrib import admin
from .models import Establecimiento
from .models import Afluente
from .models import Departamento
from .models import Localidad
# Register your models here.

admin.site.register(Establecimiento)
admin.site.register(Afluente)
admin.site.register(Departamento)
admin.site.register(Localidad)