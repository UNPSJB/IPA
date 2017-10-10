from django.db import models

class Edicto(models.Model):
	numero = models.CharField(max_length=10)
	fechaPublicacion = models.DateField()
	fechaExigencia = models.DateField()
#	expediente = models.ForeignKey('expediente.Expediente')