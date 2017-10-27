from django.db import models
from apps.personas.models import Persona
from apps.establecimientos.models import Establecimiento


# Create your models here.

class InfraccionActa(models.Model):
	numero = models.IntegerField()
	fecha = models.DateField()
	oficialSumariante = models.ForeignKey(Persona)
	descripcion = models.CharField(max_length=100)
	# estado = models. 
	fechaArchivado = models.DateField()
	# escaneado = models.	
	establecimiento = models.ForeignKey(Establecimiento)
			
	
	def __str__(self):
		return self.numero