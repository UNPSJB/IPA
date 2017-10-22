from django.db import models

from apps.personas.models import Persona
from apps.localidad.models import Localidad

# Create your models here.
class Establecimiento(models.Model):
	duenio = models.ForeignKey(Persona)
	codigoCatastral = models.CharField(max_length=100, primary_key = True)
	superficie = models.IntegerField()
	nombre = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=100)
	localidad = models.ForeignKey(Localidad)

	def __str__(self):
		return self.nombre + " | " + self.codigoCatastral