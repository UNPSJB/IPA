# -- encoding: utf-8 --
from __future__ import unicode_literals

from django.db import models
from django.db.models import Q, F, Value
from django.db.models.functions import Concat

# Create your models here.
class Persona(models.Model):

	tipoRol = [ 
		'Director', 
		'Administrativo', 
		'Inspector', 
		'JefeDepartamento', 
		'Chofer', 
		'Solicitante', 
		'Liquidador', 
		'Sumariante'
	]

	TipoDocumento = [
		('1', 'DNI'),
		('2', 'LC'),
		('3', 'LE'),
		('4', 'PASS'),
		('5', 'CUIL')
	]

	class Meta:
		unique_together = ("tipoDocumento", "numeroDocumento")
		ordering = ["nombre", "apellido"]
		permissions = (
			("listar_persona","Listar personas"),
			("cargar_persona","Cargar personas"),
			("modificar_persona","Modificar personas"),
			("detalle_persona","Ver detalle de personas"),
			("eliminar_persona","Eliminar personas")
		)

	nombre = models.CharField(max_length=30)
	apellido = models.CharField(max_length=30)
	email = models.EmailField()
	tipoDocumento = models.CharField(max_length=1, choices=TipoDocumento)
	numeroDocumento = models.CharField(max_length=13, unique=True)
	direccion = models.CharField(max_length=60)
	telefono = models.CharField(max_length=11)

	def __str__(self):
		return "{}, {}".format(self.apellido, self.nombre)

	@property
	def nombre_completo(self):
		return "{} {}".format(self.nombre, self.apellido)

	def es_director(self):
		return self.sos(Director)

	def es_chofer(self):
		return self.sos(Chofer)

	def como(self, Klass):
		return self.roles.get(tipo=Klass.TIPO).related()

	def como_director(self):
		return self.como(Director)

	def como_chofer(self):
		return self.como(Chofer)

	def agregar_rol(self, rol):
		if not self.sos(rol.__class__):
			rol.persona = self
			rol.save()
			
	def roles_related(self):
		return [rol.related() for rol in self.roles.all()]

	def sos(self, Klass):
		return any([isinstance(rol, Klass) for rol in self.roles_related()])
	
	def getRolesName(self):
		lista_de_roles = [rol.__class__.__name__ for rol in self.roles_related()]
		cadena_de_retorno = '['
		for i in lista_de_roles:
			cadena_de_retorno += "'" + i + "'" + ","
		cadena_de_retorno += ']'
		return cadena_de_retorno

	def getRolesNameTemplate(self):
		lista_de_roles = [rol.__class__.__name__ for rol in self.roles_related()]
		cadena_de_retorno = '['
		for r in lista_de_roles:
			cadena_de_retorno += r + ", "
		cadena_de_retorno = cadena_de_retorno[:-2]+ ']'
		return cadena_de_retorno
	
	def getRolesParaComisionNames(self):
		lista_de_roles = [rol.get_tipo_display() for rol in self.roles.filter(tipo__in=[3,4,7])]
		cadena_de_retorno = '['
		for i in lista_de_roles:
			cadena_de_retorno += i + ' | '
		cadena_de_retorno = cadena_de_retorno[:-3]+']'
		return cadena_de_retorno

	@classmethod
	def getEmpleadosParaComision(Klass):
		return Persona.objects.all().filter(roles__tipo__in=[3,4,7]).order_by('id').distinct('id')

	def empresas_list(self):
		return list(self.empresa_set.values_list('cuit', flat=True))

	def getDirectorData(self):
		return {}

	def getChoferData(self):
		self.como(Chofer)

	@classmethod
	def choices(cls):
		return cls.objects.annotate(nombre_completo=Concat(F('nombre'), Value(' '), F('apellido'), output_field=models.CharField())).values('id', 'nombre_completo')


class Rol(models.Model):
	TIPO = 0
	TIPOS = [ (0, "rol") ]

	persona = models.ForeignKey(Persona,on_delete=models.CASCADE,null=True, related_name="roles")
	tipo = models.PositiveSmallIntegerField(choices=TIPOS)
	
	def save(self, *args, **kwargs):
		if self.pk is None:
			self.tipo = self.__class__.TIPO
		super(Rol, self).save(*args, **kwargs)

	def related(self):
		if self.__class__ != Rol:
			return self
		else:
			#return self.get_tipo_display()
			return getattr(self, self.get_tipo_display())

	@classmethod
	def register(cls, klass):
		cls.TIPOS.append((klass.TIPO, klass.__name__.lower()))

	def __str__(self):
		return "{rol}".format(rol=self.__class__.__name__)

	def getInfo(self):
		return { 's':  'aa',  'otra': 'cosa'}

	def roleName(self):
		return 'N/N'

	def es(self, rol):
		return str(self) == rol

	def es_director(self):
		return self.es('Director')

	def es_chofer(self):
		return self.es('Chofer')
		
class Director(Rol):
	TIPO = 1
	legajo =  models.IntegerField()
	cargo = models.CharField(max_length=25)
	fechaInicio = models.DateField()

	@classmethod
	def roleName(self):
		return 'Director'


class Administrativo(Rol):
	TIPO = 2

	def roleName(self):
		return 'Administrativo'

class Inspector(Rol):
	TIPO = 3

	def roleName(self):
		return 'Inspector'
	
class JefeDepartamento(Rol):
	TIPO = 8

	def roleName(self):
		return 'Jefe de departamento'


class Chofer(Rol):
	TIPO = 4
	licencia = models.CharField(max_length=20)
	vencimientoLicencia = models.DateField()

	def roleName(self):
		return 'Chofer'


class Solicitante(Rol):
	TIPO = 5
	
	def roleName(self):
		return 'Solicitante'

class Liquidador(Rol):
	TIPO = 6

	def roleName(self):
		return 'Liquidador'
	
class Sumariante(Rol):
	TIPO = 7

	def roleName(self):
		return 'Sumariante'
	
for Klass in Persona.tipoRol:
    Rol.register(eval(Klass))

class Empresa(models.Model):
	cuit = models.CharField(max_length=13, unique=True)
	razonSocial = models.CharField(max_length=30, null=True, blank=True)
	direccion = models.CharField(max_length=60)
	telefono = models.CharField(max_length=11)
	representantes = models.ManyToManyField(Persona)

	def __unicode__(self):
		return self.razonSocial

	def __str__(self):
		return "{} - {}".format(self.cuit, self.razonSocial)

	def tiene_representantes(self):
		return self.representantes.all().count() > 0

	class Meta:
		permissions = (
			("cargar_empresa","Cargar empresas"),
			("detalle_empresa","Ver detalle de empresas"),
			("listar_empresa","Listar empresas"),
			("modificar_empresa","Modificar empresas"),
			("eliminar_empresa","Eliminar empresas")
		)
		ordering = ['razonSocial']