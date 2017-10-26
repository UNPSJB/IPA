from django.db import models
from apps.personas.models import Persona
# Create your models here.


class Oposicion(models.Model):
	numero = models.CharField(max_length=30)
	persona = models.ForeignKey(Persona, null=False, blank=False)
	fecha = models.DateField()
	descripcion = models.TextField()
	documento = models.CharField(max_length=100)

	class Meta:
		ordering = ["-numero"]

	def __str__(self):
		return self.numero