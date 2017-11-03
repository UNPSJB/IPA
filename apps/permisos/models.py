from django.db import models
from apps.personas.models import Persona
from apps.establecimientos.models import Afluente
from apps.documentos.models import Documento, TipoDocumento

# Create your models here.

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

class TipoUso(models.Model):
	tipoMedida = (
    ('0', 'unidad'),
    ('1', 'm'),
    ('2', 'm2'),
    ('3', 'm3'),
    ('4', 'Ha'),
    ('5', 'KW'),
	)

	tipoPeriodo = (
	('0', 'hora'),
	('1', 'dia'),
	('2', 'mes'),
	('3', 'año'),
	) 

	nombre = models.CharField(max_length=50)
	coeficiente = models.IntegerField()
	periodo = models.CharField(max_length=1, choices=tipoPeriodo)
	medida = models.CharField(max_length=1, choices=tipoMedida)
	documentos = models.ManyToManyField(TipoDocumento)

	def __str__(self):
		return self.nombre

class Permiso(models.Model):
	solicitante = models.ForeignKey('personas.Solicitante')
	establecimiento = models.ForeignKey('establecimientos.Establecimiento')
	tipo = models.ForeignKey(TipoUso)
	afluente = models.ForeignKey(Afluente)
	numero_exp = models.PositiveIntegerField(null=True)
	documentos = models.ManyToManyField(Documento)


	objects = PermisoManager()

	def estado(self):
		if self.estados.exists():
			return self.estados.latest().related()

	@classmethod
	def new(cls, usuario, fecha, solicitante, establecimiento, tipo, afluente):
		t = cls(tipo=tipo, solicitante=solicitante, establecimiento=establecimiento, afluente=afluente)
		t.save()
		t.hacer(None, usuario=usuario, fecha=fecha, observacion="Arranca el permiso")
		return t

	def estados_related(self):
		return [estado.related() for estado in self.estados.all()]

	def hacer(self, accion, *args, **kwargs):
		estado_actual = self.estado()
		if estado_actual is not None and hasattr(estado_actual, accion):
			metodo = getattr(estado_actual, accion)
			estado_nuevo = metodo(self, *args, **kwargs)
			if estado_nuevo is not None:
				estado_nuevo.save()
		elif estado_actual is None:
			Solicitado(permiso=self, *args, **kwargs).save()
		else:
			raise Exception("Tramite: La accion solicitada no se pudo realizar")

	def agregarDocumentacion(self, documento):
		self.documentos.add(documento)

class Estado(models.Model):
	TIPO = 0
	TIPOS = [
		(0, 'estado')
	]
	# Marca de tiempo asiganda por el sistema al crear un estado
	timestamp = models.DateTimeField(auto_now_add=True)
	# Fecha en la que ocurre fisicamente la accion (ingresada generalmente por un usuario)
	fecha = models.DateField()
	permiso = models.ForeignKey(Permiso, related_name="estados")
	tipo = models.PositiveSmallIntegerField(choices=TIPOS)
	observacion = models.CharField(max_length=300, null=True, blank=True)
	usuario = models.ForeignKey('users.Usuario', null=True, blank=True)

	class Meta:
		ordering = ["timestamp"]
		get_latest_by = 'timestamp'

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

	def recibir(self, usuario, fecha, documentos):
		for documento in documentos:
			self.permiso.documentos.add(documento)
		return self

	def revisar(self, usuario, fecha, documentos):
		for documento in documentos:
			documento.visado = True
			documento.save()
		if self.permiso.documentos.filter(documentos__visado=True).exists():
			return Visado(permiso=self.permiso, usuario=usuario, fecha=fecha)
		return self

class Visado(Estado):
	TIPO = 2
	fecha_visado = models.DateField()

	def recibir(self, usuario, fecha, documentos):
		for documento in documentos:
			self.permiso.documentos.add(documento)
		return self

	def revisar(self, usuario, fecha, documentos):
		for documento in documentos:
			documento.visado = True
			documento.save()
		return self

	def pasar(self, usuario, fecha, expediente, pase):
		self.permiso.numero_exp = expediente
		self.permiso.documentos.add(pase)
		self.permiso.save()
		return Creado(permiso=self.permiso, usuario=usuario, fecha=fecha)

class Creado(Estado):
	TIPO = 3
	""" Estado del tramite cuando se convierte en expediente """
	def recibir(self, usuario, fecha, documentos):
		for documento in documentos:
			self.permiso.documentos.add(documento)
		return self

	def revisar(self, usuario, fecha, documentos):
		for documento in documentos:
			documento.visado = True
			documento.save()
		return self

	def completar(self, usuario, fecha):
		visados = self.permiso.documentos.filter(visado=True)
		pk_tipos_requeridos = [t.pk for t in self.permiso.tipo.documentos.all()]
		pk_tipos_visados = [d.tipo.pk for d in visados]
		if set(pk_tipos_requeridos).issubset(set(pk_tipos_visados)):
			return Completado(permiso=self.permiso, usuario=usuario, fecha=fecha)
		return self

class Completado(Estado):
	TIPO = 4
	""" Estado del tramite cuando se completo la documentacion del expediente """

	def publicar(self, usuario, fecha, tiempo, edicto):
		self.permiso.documentos.add(edicto)
		return Publicado(permiso=self.permiso, usuario=usuario, fecha=fecha, tiempo=tiempo)

class Publicado(Estado):
	TIPO = 5
	# No contemplar dias habiles.... para no entrar en tema de feriados
	tiempo = models.PositiveIntegerField()

	def resolver(self, usuario, fecha, unidad, resolucion):
		if self.fecha + self.tiempo < fecha:
			self.permiso.documentos.add(resolucion)
			monto = self.permiso.tipo.calcular_monto(unidad)
			return Otorgado(permiso=self.permiso, usuario=usuario, fecha=fecha, monto=monto)
		return self

class Otorgado(Estado):
	TIPO = 6
	monto = models.DecimalField(max_digits = 10, decimal_places = 2)

	def cobrar(self, usuario, fecha, monto, pago):
		self.permiso.documentos.add(pago)
		return self

	# Recalculando monto en base a inscpeccion o capricho del director
	def recalcular(self, usuario, fecha, unidad, documento):
		self.permiso.documentos.add(documento)
		monto = self.permiso.tipo.calcular_monto(unidad)
		return Otrogado(permiso=self.permiso, usaurio=usuario, fecha=fecha, monto=monto)

for Klass in [Solicitado, Visado, Creado, Completado, Publicado, Otorgado]:
	Estado.register(Klass)

