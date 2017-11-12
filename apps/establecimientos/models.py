from django.db import models
from apps.personas.models import Persona

# Create your models here.

class Departamento(models.Model):
	nombre = models.CharField(max_length = 50)
	superficie = models.CharField(max_length = 50)
	poblacion = models.IntegerField()
	descripcion = models.TextField()

	def __str__(self):
		return '{}'.format(self.nombre)


class Localidad(models.Model):
	codpostal = models.IntegerField()
	nombre = models.CharField(max_length = 50)
	departamento = models.ForeignKey(Departamento, null=False, blank=False)

	def __str__(self):
		return self.nombre


class Establecimiento(models.Model):
	duenio = models.ForeignKey(Persona)
	codigoCatastral = models.CharField(max_length=100, primary_key = True)
	superficie = models.IntegerField()
	nombre = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=100)
	localidad = models.ForeignKey(Localidad)

	def __str__(self):
		return '{} | {}'.format(self.nombre, self.codigoCatastral)


class Afluente(models.Model):
	nombre = models.CharField(max_length=100)
	localidad = models.ForeignKey(Localidad, null=False, blank=False)
	caudal = models.CharField(max_length=100)
	longitud = models.CharField(max_length=100)
	superficie = models.CharField(max_length=100)
	descripcion = models.TextField()

	class Meta:
		ordering = ["-nombre"]

	def __str__(self):
		return self.nombre