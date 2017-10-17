# -- encoding: utf-8 --
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Persona(models.Model):
	nombre = models.CharField(max_length=30)
	apellido = models.CharField(max_length=30)
	email = models.EmailField()
	tipoDocumento = models.CharField(max_length=10)
	numeroDocumento = models.CharField(max_length=15)
	razónSocial = models.CharField(max_length=10)
	dirección = models.CharField(max_length=60)
	teléfono = models.IntegerField()

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

class Director(Rol):
	TIPO = 1

	def __init__(self):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.legajo = models.IntegerField()
		self.cargo = models.CharField(max_length=25)
		#fecha inicio de cargo
		self.fechaInicio = models.DateField()

class Administrativo(Rol):
	TIPO = 2

	def __init__(self, *args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)

class Inspector(Rol):
	TIPO = 3
	def __init__(self, *args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)

class JefeDepartamento(Rol):
	TIPO = 3
	def __init__(self, *args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)

class Chofer(Rol):
	TIPO = 4
	def __init__(self, *args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.licencia = models.CharField(max_length=20)
		self.vencimientoLicencia = models.DateField()
		#tipo ?????????????????

class Solicitante(Rol):
	TIPO = 5
	def __init__(self, *args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)

class Liquidador(Rol):
	TIPO = 6
	def __init__(self, *args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)