from django.db import models
from apps.personas.models import Persona
from apps.reclamo.models import Reclamo
from apps.establecimientos.models import *

# Create your models here.
class Comision (models.Model):
	empleado = models.ForeignKey(Persona, null=False, blank=False)
	reclamos = models.ForeignKey(Reclamo, null=False, blank=False)
	departamento = models.ForeignKey(Departamento, null=False, blank=False)
	localidad = models.ForeignKey(Localidad, null=False, blank=False)
	fechaInicio = models.CharField(max_length=100)
	fechaFin = models.CharField(max_length=100)
	

	class Meta:
		ordering = ["-fechaInicio"]

	def __str__(self):
		return self.fechaInicio
