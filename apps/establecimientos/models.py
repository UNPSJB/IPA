from django.db import models
from apps.personas.models import Persona
from django.utils.text import slugify

# Create your models here.

class DepartamentoManager(models.Manager):
	def __init__(self, protegido=False):
		super().__init__()
		self.protegido = protegido

	def get_queryset(self):
		return super().get_queryset()

# Create your models here.
class Departamento(models.Model):
	nombre = models.CharField(max_length=50)
	superficie = models.CharField(max_length = 50)
	poblacion = models.IntegerField()
	descripcion = models.TextField()
	slug = models.SlugField()
	protegido = models.BooleanField(default=False)

	objects = DepartamentoManager(True)
	protegidos = DepartamentoManager(True)

	class Meta:
		permissions = (
			("cargar_departamento","Cargar deparamentos"),
			("modificar_departamento","Modificar deparamentos"),
			("detalle_departamento","Ver detalle de deparamentos"),
			("listar_departamento","Listar deparamentos"),
			("eliminar_departamento","Eliminar deparamentos")
		)


	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.nombre)
		return super().save(*args, **kwargs)
	
	def __str__(self):
		return self.nombre

	@classmethod
	def get_protegido(klass, slug):
		return klass.protegidos.get(slug=slug)


class LocalidadManager(models.Manager):
	def __init__(self, protegido=False):
		super().__init__()
		self.protegido = protegido

	def get_queryset(self):
		return super().get_queryset().filter()


class Localidad(models.Model):
	codpostal = models.IntegerField(unique=False)
	nombre = models.CharField(max_length = 50)
	departamento = models.ForeignKey(Departamento, null=False, blank=False)
	slug = models.SlugField()
	protegido = models.BooleanField(default=False)

	objects = LocalidadManager(False)
	protegidos = LocalidadManager(True)
	
	class Meta:
		permissions = (
			("cargar_localidad","Cargar localidades"),
			("modificar_localidad","Modificar localidaes"),
			("listar_localidad","Listar localidades"),
			("eliminar_localidad","Eliminar localidades")
		)
		ordering : ['nombre']

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.nombre)
		return super().save(*args, **kwargs)
	
	def __str__(self):
		return self.nombre

	@classmethod
	def get_protegido(klass, slug):
		return klass.protegidos.get(slug=slug)

	def __unicode__(self):
		return self.nombre


class Establecimiento(models.Model):
	duenio = models.ForeignKey(Persona)
	codigoCatastral = models.CharField(max_length=100, primary_key = True)
	superficie = models.IntegerField()
	nombre = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=500)
	localidad = models.ForeignKey(Localidad)

	def __str__(self):
		return '{} | {}'.format(self.nombre, self.codigoCatastral)

	class Meta:
		ordering = ['nombre']
		permissions = (
			("cargar_establecimiento","Cargar establecimientos"),
			("listar_establecimiento","Listar establecimientos"),
			("detalle_establecimiento","Ver detalle de establecimientos"),
			("modificar_establecimiento","Modificar establecimientos"),
			("eliminar_establecimiento","Eliminar establecimientos")
		)

class Afluente(models.Model):
	nombre = models.CharField(max_length=100)
	localidad = models.ForeignKey(Localidad, null=False, blank=False)
	caudal = models.CharField(max_length=100)
	longitud = models.CharField(max_length=100)
	superficie = models.CharField(max_length=100)
	descripcion = models.TextField()

	class Meta:
		ordering = ["-nombre"]
		permissions = (
			("cargar_afluente","Cargar afluentes"),
			("detalle_afluente","Ver detalle de afluentes"),
			("listar_afluente","Listar afluentes"),
			("modificar_afluente","Modificar afluentes"),
			("eliminar_afluente","Eliminar afluentes")
		)

	def __str__(self):
		return self.nombre