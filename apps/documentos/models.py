from django.db import models

# Create your models here.
class TipoDocumento(models.Model):
	nombre = models.CharField(max_length=50)

	class Meta:
		ordering = ["-nombre"]

	def __str__(self):
		return self.nombre

class Documento(models.Model):
	tipo = models.ForeignKey(TipoDocumento, null=True, blank=True)
	descripcion = models.CharField(max_length=100)
	archivo = models.FileField()
	visado = models.BooleanField()
	fecha = models.DateField()