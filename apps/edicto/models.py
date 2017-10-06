from django.db import models
#from apps.expediente.models import Expediente

# Create your models here.
class Edicto(models.Model):
	numero = models.CharField(max_length=10)
	fecha_publicacion = models.DateField()
	fecha_maxima = models.DateField()
#	expediente = models.ForeignKey('expediente.Expediente')
