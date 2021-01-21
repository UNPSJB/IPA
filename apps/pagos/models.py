from django.db import models
#from apps.permisos.models import TipoUso
from apps.documentos.models import Documento
# Create your models here.

#lo que le deben al ipa
class Pago(models.Model):
	permiso = models.ForeignKey('permisos.Permiso', blank=False, null=False, related_name="pagos")
	monto = models.DecimalField(max_digits = 10, decimal_places = 2)
	documento = models.ForeignKey(Documento, blank=False, null=False)
	fecha = models.DateField()
	es_por_canon = models.BooleanField(default=True)

	@classmethod
	def getPagosCanon(Klass):
		return Pago.objects.all().filter(es_por_canon=True)

	@classmethod
	def getPagosInfraccion(Klass):
		return Pago.objects.all().filter(es_por_canon=False)

	def tipo_de_pago(self):
		return "Canon" if self.es_por_canon else "Infraccion"

#ipa registra el cobro
class Cobro(models.Model):
	permiso = models.ForeignKey('permisos.Permiso', blank=False, null=False, related_name="cobros")
	monto = models.DecimalField(max_digits = 10, decimal_places = 2)
	documento = models.ForeignKey(Documento, blank=False, null=False)
	fecha_desde = models.DateField()
	fecha_hasta = models.DateField()
	es_por_canon = models.BooleanField(default=True)

	class Meta:
		get_latest_by = "fecha_hasta"

	@classmethod
	def getCobrosCanon(Klass):
		return Cobro.objects.all().filter(es_por_canon=True)

	@classmethod
	def getCobrosInfraccion(Klass):
		return Cobro.objects.all().filter(es_por_canon=False)

# MODULOS ===================================================
class ValorDeModulo (models.Model):
	DIESEL = 1
	KW = 2
	TipoModulo = [
		(DIESEL, 'Diesel'),
		(KW, 'Kw')
	]
	
	modulo = models.PositiveIntegerField(choices=TipoModulo)
	precio = models.DecimalField(max_digits = 10, decimal_places = 2)
	fecha = models.DateField()
	descripcion = models.TextField()

	class Meta:
		ordering = ["fecha"]
		unique_together = ("fecha", "modulo")
		get_latest_by = "fecha"

	def __str__(self):
		return "{fecha}: ${precio}".format(fecha=self.fecha, precio=self.precio)
