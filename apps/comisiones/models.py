from django.db import models
from apps.personas.models import Persona
from apps.establecimientos.models import *
from apps.documentos.models import Documento

# Create your models here.
class Comision (models.Model):
	empleados = models.ManyToManyField(Persona, blank=False)
	documentos = models.ManyToManyField(Documento, blank=True)
	localidades = models.ManyToManyField(Localidad, blank=False)
	fechaInicio = models.DateField()
	fechaFin = models.DateField()
	

	class Meta:
		ordering = ["-fechaInicio"]
		verbose_name_plural = "Comisión"

	def __str__(self):
		return self.fechaInicio
