
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
			("cargar_tipo_documento","Cargar tipo de documentos"),
			("listar_tipo_documento","Listar tipo de documentos"),
			("modificar_tipo_documento","Modificar tipo de documentos"),
			("eliminar_tipo_documento","Eliminar tipo de documentos"),
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
	ENTREGADO = 0
	RECHAZADO = 1
	VISADO = 2
	
	Estado = [
		(ENTREGADO, 'Entregado'),
		(RECHAZADO, 'Rechazado'),
		(VISADO, 'Visado'),
	]

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
	estado = models.PositiveIntegerField(choices=Estado,default=0)
	fecha = models.DateField()

	class Meta:
		permissions = (
			("cargar_documento","Cargar documentos"),
			("detalle_documento","Ver detalle de documentos"),
			("modificar_documento","Modificar documentos"),
			("eliminar_documento","Eliminar documentos"),
			("cargar_expediente","Cargar expedientes"),
			("cargar_edicto","Cargar edictos"),
			("cargar_resolucion","Cargar resoluciones"),
			("cargar_oposicion","Cargar oposiciones"),
			("baja_permiso","Dar de baja los permisos"),
			("archivar_permiso","Archivar los permisos"),
			("cargar_acta_infraccion","Cargar actas de Infracción"),
			("cargar_acta_inspeccion","Cargar actas de inspección")
		)

	def save(self):
		thumbnail = "thumbnails/%s.png" % (datetime.now().strftime("%Y%m%d%H%M%S"),)
		self.thumbnail = thumbnail
		super(Documento, self).save()
	
	def __str__(self):
		return self.descripcion

	def verificar_transicion_estado(self,es_documento_nuevo):
		if es_documento_nuevo:
			self.estado = 0
		self.save()

	@classmethod
	def rep_inspeccion_infraccion(cls):
		T = []
		documentos = Documento.objects.filter(tipo__slug__in=['acta-de-inspeccion','acta-de-infraccion'])
		for doc in documentos:
			if doc.tipo.slug == 'acta-de-inspeccion':
				T.append({'fecha':doc.fecha,'tipo':'acta-de-inspeccion','descripcion':doc.descripcion})
			else:
				T.append({'fecha':doc.fecha,'tipo':'acta-de-infraccion','descripcion':doc.descripcion})
		return T

# Que se hace luego de guardar el documento
def pdf_post_save(sender, instance=False, **kwargs):
	"""Esta funcion crea un thumbnail para el documento en pdf"""
	documento = Documento.objects.get(pk=instance.pk)
	command = "convert -quality 95 -thumbnail 222 %s %s" % (
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

