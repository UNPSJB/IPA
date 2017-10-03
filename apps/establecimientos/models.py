from django.db import models

from apps.persona.models import Persona
from apps.localidad.models import Localidad

# Create your models here.
class Establecimiento(models.Model):
	duenio = models.ForeignKey(Persona)
	codigoCatastral = models.CharField(max_length=100)
	superficie = models.IntegerField()
	nombre = models.CharField(max_length=50)
	descripción = models.CharField(max_length=100)
	localidad = models.ForeignKey(Localidad, null=False, blank=False)

	def __str__(self):
		return self.nombre + " | " + self.codigoCatastral