from django.db import models
from apps.localidad.models import Localidad

# Create your models here.
class Afluente(models.Model):
	nombre = models.CharField(max_length=100)
	localidad = models.ForeignKey(Localidad, null=False, blank=False)
	caudal = models.CharField(max_length=100)
	longitud = models.CharField(max_length=100)
	superficie = models.CharField(max_length=100)
	descripcion = models.TextField()

	
