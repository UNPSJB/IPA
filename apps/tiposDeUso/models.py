from django.db import models

# Create your models here.

PERIOD_TYPES_CHOICES = (
    ('0', 'unidad'),
    ('1', 'm'),
    ('2', 'm2'),
    ('3', 'm3'),
    ('4', 'Ha'),
    ('5', 'KW'),
)

MEASUREMENT_UNIT_CHOICES = (
	('0', 'hora'),
    ('1', 'dia'),
    ('2', 'mes'),
    ('3', 'año'),
) 

class TipoUso(models.Model):
	nombre = models.CharField(max_length=50)
	coeficiente = models.IntegerField()
	
	periodo = models.CharField(max_length=1, choices=PERIOD_TYPES_CHOICES)
	medida = models.CharField(max_length=1, choices=MEASUREMENT_UNIT_CHOICES)
	documentos = models.ManyToManyField("tiposDocumentacion.TipoDocumentacion")

	def __str__(self):
		return self.nombre