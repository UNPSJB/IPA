from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.text import slugify
from datetime import datetime
import os
import subprocess

# Create your models here.
class TipoDocumento(models.Model):
	nombre = models.CharField(max_length=50)
	slug = models.SlugField()
	protegido = models.BooleanField(default=False)

	objects = TipoDocumentoManager(False)
	protegidos = TipoDocumentoManager(True)

	class Meta:
		ordering = ["-nombre"]

	def __str__(self):
		return self.nombre

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