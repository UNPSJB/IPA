from django.db import models


# Create your models here.
class Expediente(models.Model):
	fecha_creacion = models.DateField()
	numero = models.CharField(max_length=10)
	extracto = models.CharField(max_length=144)
#	expediente = models.ForeignKey('expediente.Expediente')
