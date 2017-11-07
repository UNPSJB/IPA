from django.db import models
#from apps.permisos.models import Permiso
from apps.documentos.models import Documento
# Create your models here.

class Pago(models.Model):
	#permiso = models.ForeignKey(Permiso, blank=False, null=False)
	monto = models.DecimalField(max_digits = 10, decimal_places = 2)
	documento = models.ForeignKey(Documento, blank=False, null=False)
	fecha = models.DateField()

class Cobro(models.Model):
	#permiso = models.ForeignKey(Permiso, blank=False, null=False)
	monto = models.DecimalField(max_digits = 10, decimal_places = 2)
	documento = models.ForeignKey(Documento, blank=False, null=False)
	fecha = models.DateField()

class Modulo(models.Model):
	TipoModulo = [
		('1', 'Dolar'),
		('2', 'EuroDiesel'),
		('3', 'UltraDiesel'),
	]

	class Meta:
		ordering = ["nombre"]
	
	codigo = models.CharField(max_length=2)
	nombre = models.CharField(max_length=1, choices=TipoModulo)
	descripcion = models.TextField()

	def __str__(self):
		return self.codigo

class RegistrarValorDeModulo (models.Model):
	modulo = models.ForeignKey(Modulo, blank=False, null=False)
	precio = models.DecimalField(max_digits = 10, decimal_places = 2)
	fecha = models.DateField()
	descripcion = models.TextField()

	class Meta:
		ordering = ["fecha"]

	def __str__(self):
		return "{fecha}: ${precio}".format(fecha=self.fecha, precio=self.precio)

class formula():
	pass