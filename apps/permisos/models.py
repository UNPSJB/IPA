from django.db import models

# Create your models here.
class Solicitud(models.Model):
	fecha_solicitud = models.DateField()
	solicitante = models.ForeignKey('personas.Persona')
	establecimiento = models.ForeignKey('establecimientos.Establecimiento')
	tipo = models.ForeignKey('tiposDeUso.TipoUso')
#	afluente = models.ForeignKey('afluentes.Afluente')
	utilizando = models.BooleanField()