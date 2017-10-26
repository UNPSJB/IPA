from django.db import models


# Create your models here.
class Expediente(models.Model):
	fecha = models.DateField()
	numero = models.CharField(max_length=10)
	extracto = models.CharField(max_length=144)
#	permiso = models.ForeignKey('expediente.Expediente')

	class Meta:
		ordering = ["-numero"]

	def __str__(self):
		return self.numero