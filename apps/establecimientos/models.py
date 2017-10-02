from django.db import models

# Create your models here.
class Establecimiento(models.Model):
	duenio = models.ForeignKey("personas.Persona")
	codigoCatastral = models.CharField(max_length=100)
	superficie = models.IntegerField()
	nombre = models.CharField(max_length=50)
	descripción = models.CharField(max_length=100)
	localidad = models.ForeignKey("localidades.Localidad")

	def __str__(self):
		return nombre + " | " + codigoCatastral