from django.db import models

# Create your models here.
class Solicitud(models.Model):
	fecha_solicitud = models.DateField()
	"""solicitante = models.ForeignKey(        
		'apps.personas.Solicitante',
        )
	establecimiento = models.ForeignKey(
		'apps.establecimientos.Establecimiento'
	)
	tipo = models.ForeignKey(
		'apps.tiposDeUso.Tipos'
		)
	afluente = models.ForeignKey(
		'apps.afluentes.Afluente'
		)"""
	utilizando = models.BooleanField()