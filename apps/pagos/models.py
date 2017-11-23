from django.db import models
#from apps.permisos.models import TipoUso
from apps.documentos.models import Documento
# Create your models here.

#lo que le deben al ipa
class Pago(models.Model):
	permiso = models.ForeignKey('permisos.Permiso', blank=False, null=False)
	monto = models.DecimalField(max_digits = 10, decimal_places = 2)
	documento = models.ForeignKey(Documento, blank=False, null=False)
	fecha = models.DateField()

#ipa registra el cobro
class Cobro(models.Model):
	permiso = models.ForeignKey('permisos.Permiso', blank=False, null=False)
	monto = models.DecimalField(max_digits = 10, decimal_places = 2)
	documento = models.ForeignKey(Documento, blank=False, null=False)
	fecha = models.DateField()

# MODULOS ===================================================
class ValorDeModulo (models.Model):
	#modulo = models.PositiveIntegerField(choices=TipoUso.TipoModulo)
	modulo = models.PositiveIntegerField()
	precio = models.DecimalField(max_digits = 10, decimal_places = 2)
	fecha = models.DateField()
	descripcion = models.TextField()

	class Meta:
		ordering = ["fecha"]
		unique_together = ("fecha", "modulo")

	def __str__(self):
		return "{fecha}: ${precio}".format(fecha=self.fecha, precio=self.precio)
