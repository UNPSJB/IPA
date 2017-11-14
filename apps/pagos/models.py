from django.db import models
#from apps.permisos.models import Permiso
from apps.documentos.models import Documento
# Create your models here.

#lo que le deben al ipa
class Pago(models.Model):
	#permiso = models.ForeignKey(Permiso, blank=False, null=False)
	monto = models.DecimalField(max_digits = 10, decimal_places = 2)
	documento = models.ForeignKey(Documento, blank=False, null=False)
	fecha = models.DateField()

#ipa registra el cobro
class Cobro(models.Model):
	#permiso = models.ForeignKey(Permiso, blank=False, null=False)
	monto = models.DecimalField(max_digits = 10, decimal_places = 2)
	documento = models.ForeignKey(Documento, blank=False, null=False)
	fecha = models.DateField()

# MODULOS ===================================================
class RegistrarValorDeModulo (models.Model):
	#modulo = models.ForeignKey(Modulo, blank=False, null=False)
	precio = models.DecimalField(max_digits = 10, decimal_places = 2)
	fecha = models.DateField()
	descripcion = models.TextField()

	class Meta:
		ordering = ["fecha"]

	def __str__(self):
		return "{fecha}: ${precio}".format(fecha=self.fecha, precio=self.precio)
