from django.db import models
from apps.personas.models import Persona

# Create your models here.

class DepartamentoManager(models.Manager):
	def __init__(self, protegido=False):
		super().__init__()
		self.protegido = protegido

	def get_queryset(self):
		return super().get_queryset().filter(protegido=self.protegido)

# Create your models here.
class Departamento(models.Model):
	nombre = models.CharField(max_length=50)
	superficie = models.CharField(max_length = 50)
	poblacion = models.IntegerField()
	descripcion = models.TextField()
	slug = models.SlugField()
	protegido = models.BooleanField(default=False)

	objects = DepartamentoManager(False)
	protegidos = DepartamentoManager(True)
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
	
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.nombre)
		return super().save(*args, **kwargs)
	
	def __str__(self):
		return self.nombre

	@classmethod
	def get_protegido(klass, slug):
		return klass.protegidos.get(slug=slug)


class Establecimiento(models.Model):
	duenio = models.ForeignKey(Persona)
	codigoCatastral = models.CharField(max_length=100, primary_key = True)
	superficie = models.IntegerField()
	nombre = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=500)
	localidad = models.ForeignKey(Localidad)

	def __str__(self):
		return '{} | {}'.format(self.nombre, self.codigoCatastral)


class Afluente(models.Model):
	nombre = models.CharField(max_length=100)
	localidad = models.ForeignKey(Localidad, null=False, blank=False)
	caudal = models.CharField(max_length=100)
	longitud = models.CharField(max_length=100)
	superficie = models.CharField(max_length=100)
	descripcion = models.TextField()

	class Meta:
		ordering = ["-nombre"]

	def __str__(self):
		return self.nombre