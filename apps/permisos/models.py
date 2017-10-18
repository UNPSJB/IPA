from django.db import models

# Create your models here.
class Solicitud(models.Model):
	fecha_solicitud = models.DateField()
	solicitante = models.ForeignKey('personas.Persona')
	establecimiento = models.ForeignKey('establecimientos.Establecimiento')
	tipo = models.ForeignKey('tiposDeUso.TipoUso')
	afluente = models.ForeignKey('afluente.Afluente')
	utilizando = models.BooleanField()



class PermisoBaseManager(models.Manager):
	pass

class PermisoQuerySet(models.QuerySet):
	def en_estado(self, estados):
		if type(estados) != list:
			estados = [estados]
		return self.annotate(max_id=models.Max('estados__id')).filter(
			estados__id=models.F('max_id'),
			estados__tipo__in=[ e.TIPO for e in estados])

PermisoManager = PermisoBaseManager.from_queryset(PermisoQuerySet)

class Documento(models.Model):
	permiso = models.ForeignKey('Permiso', related_name="documentos")
	nombre = models.CharField(max_length=100)
	archivo = models.FileField()
	visado = models.BooleanField()

class Permiso(models.Model):
	solicitante = models.ForeignKey('personas.Solicitante')
	establecimiento = models.ForeignKey('establecimientos.Establecimiento')
	tipo = models.ForeignKey('tiposDeUso.TipoUso')
	afluente = models.ForeignKey('afluente.Afluente')
	numero_exp = models.PositiveIntegerField(null=True)


	objects = PermisoManager()

	def estado(self):
		if self.estados.exists():
			return self.estados.latest().related()

	@classmethod
	def new(cls, tipo):
		t = cls(tipo=tipo)
		t.save()
		t.hacer(None, observacion="Arranca el permiso")
		return t

	def estados_related(self):
		return [estado.related() for estado in self.estados.all()]

	def hacer(self, accion, *args, **kwargs):
		estado_actual = self.estado()
		if estado_actual is not None and hasattr(estado_actual, accion):
			metodo = getattr(estado_actual, accion)
			estado_nuevo = metodo(self, *args, **kwargs)
			if estado_actual is not None:
				estado_nuevo.save()
		elif estado_actual is None:
			Iniciado(permiso=self, *args, **kwargs).save()
		else:
			raise Exception("Tramite: La accion solicitada no se pudo realizar")

class Estado(models.Model):
	TIPO = 0
	TIPOS = [
		(0, 'estado')
	]
	fecha = models.DateField()
	timestamp = models.DateTimeField(auto_now_add=True)
	permiso = models.ForeignKey(Permiso, related_name="estados")
	tipo = models.PositiveSmallIntegerField(choices=TIPOS)
	usuario = models.ForeignKey('users.Usuario', null=True, blank=True)

	class Meta:
		get_latest_by = 'marca'

	def save(self, *args, **kwargs):
		if self.pk is None:
			self.tipo = self.__class__.TIPO
		super(Estado, self).save(*args, **kwargs)

	def related(self):
		return self.__class__ != Estado and self or getattr(self, self.get_tipo_display())

	@classmethod
	def register(cls, klass):
		cls.TIPOS.append((klass.TIPO, klass.__name__.lower()))

class Solicitado(Estado):
	TIPO = 1
	utilizando = models.BooleanField(default=False)


class Iniciado(Estado):
	TIPO = 2
	fecha_iniciado = models.DateField()
	#observacion = models.CharField(max_length=100)

	def recibir(self, permiso, documentos):
		#permiso.documentos.add(documentos)
		return self

	def revisar(self, permiso, documentos):
		if permiso.documentos.exists():
			return Visado(permiso=permiso)
		return self

class Visado(Estado):
	TIPO = 3
	fecha_visado = models.DateField()

	def recibir(self, permiso, documentos):
		#permiso.documentos.add(documentos)
		pass

	def revisar(self, permiso, documentos):
		pass

	def pasar(self, permiso, expediente, documentos):
		permiso.numero = expediente
		#permiso.documentos.add(documentos)
		permiso.save()
		return Creado(permiso=permiso)

class Creado(Estado):
	TIPO = 4
	""" Estado del tramite cuando se convierte en expediente """
	def completar(self):
		pass

class Completado(Estado):
	TIPO = 5
	""" Estado del tramite cuando se completo la documentacion del expediente """

class Publicado(Estado):
	TIPO = 6
	edicto = models.ForeignKey('edicto.Edicto')

	def resolver(self, resolucion, documentos):
		pass

class Otorgado(Estado):
	TIPO = 7    

class Vencido(Estado):
	TIPO = 8


for Klass in [Solicitado, Iniciado, Visado, Creado, Completado, Publicado, Otorgado, Vencido]:
	Estado.register(Klass)
