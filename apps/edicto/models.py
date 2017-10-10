from django.db import models

class Expediente(models.Model):
	numero = models.CharField(max_length=10)
	fecha_creacion = models.DateField()
	fecha_maxima = models.DateField()
#	expediente = models.ForeignKey('expediente.Expediente')