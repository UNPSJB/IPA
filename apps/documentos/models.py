
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.text import slugify
from datetime import datetime
import os
import subprocess

class TipoDocumentoManager(models.Manager):
	def __init__(self, protegido=False):
		super().__init__()
		self.protegido = protegido

	def get_queryset(self):
		return super().get_queryset().filter(protegido=self.protegido)

# Create your models here.
class TipoDocumento(models.Model):
	nombre = models.CharField(max_length=50)
	slug = models.SlugField()
	protegido = models.BooleanField(default=False)

	objects = TipoDocumentoManager(False)
	protegidos = TipoDocumentoManager(True)

	class Meta:
		ordering = ["-nombre"]
		permissions = (
			("cargar_acta_inspeccion", "Puede cargar actas de inspeccion"),
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


class Documento(models.Model):
	tipo = models.ForeignKey(TipoDocumento, null=True, blank=True)
	descripcion = models.CharField(max_length=100)
	archivo = models.FileField(upload_to="documentos/%Y/%m/%d/")
	thumbnail = models.ImageField(
		verbose_name = 'Thumbnail',
		help_text = 'The thumbnail',
		upload_to = 'thumbnails/',
		blank = True, 
		null = True
	)
	visado = models.BooleanField(default=False)
	fecha = models.DateField()

	def save(self):
		thumbnail = "thumbnails/%s.png" % (datetime.now().strftime("%Y%m%d%H%M%S"),)
		self.thumbnail = thumbnail
		super(Documento, self).save()
	
	def __str__(self):
		return self.descripcion

# Que se hace luego de guardar el documento
def pdf_post_save(sender, instance=False, **kwargs):
	"""Esta funcion crea un thumbnail para el documento en pdf"""
	documento = Documento.objects.get(pk=instance.pk)
	command = "convert -quality 95 -thumbnail 222 %s[0] %s" % (
		os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, str(documento.archivo)),
		os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, str(documento.thumbnail)))
	
	proc = subprocess.Popen(command,
		shell=True,
		stdin=subprocess.PIPE,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
	)
	stdout_value = proc.communicate()[0]
	
# Hook up the signal
post_save.connect(pdf_post_save, sender=Documento)

