from django.db import models
from apps.personas.models import Persona
from apps.establecimientos.models import *
from apps.documentos.models import Documento
from datetime import date

# Create your models here.
class Comision (models.Model):
	empleados = models.ManyToManyField(Persona, blank=False)
	documentos = models.ManyToManyField(Documento)
	localidades = models.ManyToManyField(Localidad, blank=False)
	fechaInicio = models.DateField()
	fechaFin = models.DateField()
	

	class Meta:
		ordering = ["-fechaInicio"]
		verbose_name_plural = "Comisión"

	def __str__(self):
		fechaInicio = self.fechaInicio.strftime('%d/%m/%Y')
		fechaFin = self.fechaFin.strftime('%d/%m/%Y')
		return '{} | {} - {}'.format(self.id, fechaInicio, fechaFin)