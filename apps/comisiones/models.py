from django.db import models
from apps.personas.models import Persona
from apps.establecimientos.models import *
from apps.documentos.models import Documento
from datetime import date
from django.db.models import Q


# Create your models here.
class Comision (models.Model):
	nota = models.CharField(max_length=20)
	fechaInicio = models.DateField()
	fechaFin = models.DateField()
	motivo = models.TextField(max_length=200)
	empleados = models.ManyToManyField(Persona, blank=False)
	documentos = models.ManyToManyField(Documento)
	localidades = models.ManyToManyField(Localidad, blank=False)
	

	class Meta:
		ordering = ["-fechaInicio"]
		verbose_name_plural = "Comisión"
		permissions =(
			("cargar_comision","Cargar comisiones"),
			("detalle_comision","Ver detalle de comisiones"),
			("listado_comision","Listar comisiones"),
			("modificar_comision","Modificar comisiones"),
			("eliminar_comision","Eliminar comisiones")
		)

	def __str__(self):
		fechaInicio = self.fechaInicio.strftime('%d/%m/%Y')
		fechaFin = self.fechaFin.strftime('%d/%m/%Y')
		empleados = ''
		for e in self.empleados.all().values_list('nombre','apellido'):
			empleados += e[0]+', '+e[1] + ' - '

		return '{} | {} - {} | {}'.format(self.id, fechaInicio, fechaFin, empleados[:-3])

	def agregar_documentacion(self, documento):
		self.documentos.add(documento)

	@classmethod
	def getUltimas(self):
		return Comision.objects.order_by('-fechaInicio')[:20]

	@classmethod
	def rep_comisiones(cls,documentos):
		T = []

		comisiones = Comision.objects.filter(documentos__in=documentos).distinct()

		for com in comisiones:
			T.append({'fecha':com.fechaInicio,'tipo':'comision','descripcion':com.motivo})
		return T
		