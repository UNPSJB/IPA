from django.db import models

# Create your models here.
class Modulo(models.Model):
	codigo = models.CharField(max_length=2)
	nombre = models.CharField(max_length=100)
	descripcion = models.TextField()


	class Meta:
		ordering = ["-codigo"]

	def __str__(self):
		return self.codigo