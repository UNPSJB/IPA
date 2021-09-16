from django.db import models
from apps.personas.models import Persona
from apps.establecimientos.models import *
from apps.documentos.models import Documento
from datetime import date



# Create your models here.
class Comision (models.Model):
	nota = models.CharField(max_length=20)
	fechaInicio = models.DateField()
	fechaFin = models.DateField()
	motivo = models.TextField(max_length=200)
	empleados = models.ManyToManyField(Persona, blank=False)
	documentos = models.ManyToManyField(Documento)
	localidades = models.ManyToManyField(Localidad, blank=False)
	

	class Meta:
		ordering = ["-fechaInicio"]
		verbose_name_plural = "Comisión"

	def __str__(self):
		fechaInicio = self.fechaInicio.strftime('%d/%m/%Y')
		fechaFin = self.fechaFin.strftime('%d/%m/%Y')
		empleados = ''
		for e in self.empleados.all().values_list('nombre','apellido'):
			empleados += e[0]+', '+e[1] + ' - '

		return '{} | {} - {} | {}'.format(self.id, fechaInicio, fechaFin, empleados[:-3])

	def agregar_documentacion(self, documento):
		self.documentos.add(documento)

	@classmethod
	def getUltimas(self):
		return Comision.objects.order_by('-fechaInicio')[:20]

