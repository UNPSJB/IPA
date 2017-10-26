from django.db import models

# Create your models here.





class TipoUso(models.Model):
	tipoMedida = (
    ('0', 'unidad'),
    ('1', 'm'),
    ('2', 'm2'),
    ('3', 'm3'),
    ('4', 'Ha'),
    ('5', 'KW'),
	)

	tipoPeriodo = (
	('0', 'hora'),
	('1', 'dia'),
	('2', 'mes'),
	('3', 'año'),
	) 

	nombre = models.CharField(max_length=50)
	coeficiente = models.IntegerField()
	periodo = models.CharField(max_length=1, choices=tipoPeriodo)
	medida = models.CharField(max_length=1, choices=tipoMedida)
	documentos = models.ManyToManyField("tiposDocumentacion.TipoDocumentacion")

	def __str__(self):
		return self.nombre