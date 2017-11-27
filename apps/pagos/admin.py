from django.contrib import admin

from .models import ValorDeModulo, Cobro, Pago
# Register your models here.
admin.site.register(Cobro)
admin.site.register(Pago)
admin.site.register(ValorDeModulo)