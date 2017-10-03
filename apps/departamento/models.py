from django.db import models

# Create your models here.
class Departamento(models.Model):
	nombre = models.CharField(max_length = 50)
	superficie = models.CharField(max_length = 50)
	poblacion = models.IntegerField()
	descripción = models.TextField()

	def __str__(self):
		return '{}'.format(self.nombre)