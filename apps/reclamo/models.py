from django.db import models
from apps.personas.models import Persona

# Create your models here.
class Reclamo(models.Model):
	persona = models.ForeignKey(Persona, null=False, blank=False)
	lugar = models.CharField(max_length=100)
	fecha = models.DateField(max_length=100)
	motivo = models.TextField()

	class Meta:
		ordering = ["-persona"]

	def __str__(self):
		return self.persona