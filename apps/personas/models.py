# -- encoding: utf-8 --
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Persona(models.Model):

	TipoDocumento = (
		('1', 'DNI'),
		('2', 'LC'),
		('3', 'LE'),
		('4', 'PASS'),
		('5', 'CUIT')
	)

	class Meta:
		unique_together = ("tipoDocumento", "numeroDocumento")


	nombre = models.CharField(max_length=30)
	apellido = models.CharField(max_length=30)
	email = models.EmailField()
	tipoDocumento = models.CharField(max_length=1, choices=TipoDocumento)
	numeroDocumento = models.CharField(max_length=13)
	razonSocial = models.CharField(max_length=30, null=True)
	direccion = models.CharField(max_length=60)
	telefono = models.IntegerField()

	def __str__(self):
		return "{}, {}".format(self.apellido, self.nombre)

	def como(self, Klass):
		return self.roles.get(tipo=Klass.TIPO).related()

	def agregar_rol(self, rol):
		if not self.sos(rol.__class__):
			rol.persona = self
			rol.save()
			
	def roles_related(self):
		return [rol.related() for rol in self.roles.all()]

	def sos(self, Klass):
		return any([isinstance(rol, Klass) for rol in self.roles_related()])
		

class Rol(models.Model):
	TIPO = 0
	TIPOS = [ (0, "rol") ]

	persona = models.ForeignKey(Persona,on_delete=models.CASCADE,null=True, related_name="roles")
	
	def save(self, *args, **kwargs):
		if self.pk is None:
			self.tipo = self.__class__.TIPO
		super(Rol, self).save(*args, **kwargs)

	def related(self):
		if self.__class__ != Rol:
			return self
		else:
			return getattr(self, self.get_tipo_display())

	@classmethod
	def register(cls, klass):
		cls.TIPOS.append((klass.TIPO, klass.__name__.lower()))

	def __str__(self):
		return "{rol}: {persona}".format(rol=self.__class__.__name__, persona=self.persona)

class Director(Rol):
	TIPO = 1
	legajo =  models.IntegerField()
	cargo = models.CharField(max_length=25)
	fechaInicio = models.DateField()

class Administrativo(Rol):
	TIPO = 2

class Inspector(Rol):
	TIPO = 3
	
class JefeDepartamento(Rol):
	TIPO = 3

class Chofer(Rol):
	TIPO = 4
	licencia = models.CharField(max_length=20)
	vencimientoLicencia = models.DateField()

class Solicitante(Rol):
	TIPO = 5
	
class Liquidador(Rol):
	TIPO = 6
	
class Sumariante(Inspector):
	TIPO = 7
	