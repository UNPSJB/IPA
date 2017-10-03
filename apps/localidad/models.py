from django.db import models
from apps.departamento.models import Departamento

# Create your models here.

class Localidad(models.Model):
	codpostal = models.IntegerField()
	nombre = models.CharField(max_length = 50)
	departamento = models.ForeignKey(Departamento, null=False, blank=False)

	def __str__(self):
		return '{}'.format(self.nombre)