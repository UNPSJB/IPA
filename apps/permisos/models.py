from django.db import models
from apps.personas.models import Persona
from apps.establecimientos.models import Afluente
from apps.documentos.models import Documento, TipoDocumento
from apps.pagos.models import Cobro
from datetime import timedelta, date
from apps.pagos.models import ValorDeModulo

from decimal import *

# PERMISOS =================================================
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
	UNIDAD = 1
	METRO = 2
	METRO2 = 3
	METRO3 = 4
	HECTAREA = 5
	KILOWATTS = 6
	TipoMedida = (
    	(UNIDAD, 'unidad'),
    	(METRO, 'm'),
    	(METRO2, 'm2'),
    	(METRO3, 'm3'),
    	(HECTAREA, 'Ha'),
    	(KILOWATTS, 'KW'),
	)

	HORA = 1
	DIA = 1 * 24 * HORA
	MES = 1 * 30 * DIA
	ANIO = 1 * 12 * MES 
	TipoPeriodo = (
		(HORA, 'hora'),
		(DIA, 'dia'),
		(MES, 'mes'),
		(ANIO, 'año'),
	)
	TipoPeriodoDict = dict(TipoPeriodo)

	DIESEL = 1
	KW = 2
	TipoModulo = [
		(DIESEL, 'Diesel'),
		(KW, 'Kw')
	]
	TipoModuloDict = dict(TipoModulo)

	descripcion = models.CharField(max_length=500)
	coeficiente = models.DecimalField(decimal_places=2, max_digits=10)
	tipo_modulo = models.PositiveIntegerField(choices=TipoModulo)
	periodo = models.PositiveIntegerField(choices=TipoPeriodo)
	medida = models.PositiveIntegerField(choices=TipoMedida)
	documentos = models.ManyToManyField(TipoDocumento)

	def getPeriodoString(self):
		for tupla in TipoUso.TipoPeriodo:
			if tupla[0] == self.periodo:
				return tupla[1]
		return None

	def getTipoModuloString(self):
		for tupla in TipoUso.TipoModulo:
			if tupla[0] == self.tipo_modulo:
				return tupla[1]
		return None

	def getMedidaString(self):
		for tupla in TipoUso.TipoMedida:
			if tupla[0] == self.medida:
				return tupla[1]
		return None

	def __str__(self):
		return self.descripcion

	def calcular_monto(self, modulo, unidad, desde, hasta):
		dias = (hasta - desde).days
		horas = dias * 24
		lapso = horas / self.periodo
		monto = round(self.coeficiente * Decimal(modulo) * unidad * Decimal(lapso),2)
		return monto

class Permiso(models.Model):
	solicitante = models.ForeignKey(Persona)
	establecimiento = models.ForeignKey('establecimientos.Establecimiento')
	tipo = models.ForeignKey(TipoUso)
	afluente = models.ForeignKey(Afluente)
	numero_exp = models.PositiveIntegerField(null=True)
	documentos = models.ManyToManyField(Documento)
	unidad = models.DecimalField(decimal_places=2, max_digits=10, null=True)
	fechaSolicitud = models.DateField()
	fechaVencimiento = models.DateField(null=True)


	objects = PermisoManager()

	ESTADOS = [
		'Solicitado',
		'Corregido', 
		'Visado', 
		'Completado', 
		'Publicado', 
		'Otorgado', 
		'Baja'
	]

	def getEstados(self, tipo):
		return [estado for estado in self.estados_related() if estado.tipo == tipo]

	@property
	def estado(self):
		if self.estados.exists():
			return self.estados.latest().related()

	def volver_estado_anterior(self):
		if self.estados.exists():
			self.estados.latest().related().delete()

	@classmethod
	def new(cls, usuario, fecha, solicitante, establecimiento, tipo, afluente):
		t = cls(tipo=tipo, solicitante=solicitante, establecimiento=establecimiento, afluente=afluente)
		t.save()
		t.hacer(None, usuario=usuario, fecha=fecha, observacion="Arranca el permiso")
		return t

	def estados_related(self):
		return [estado.related() for estado in self.estados.all()]

	def hacer(self, accion, *args, **kwargs):
		estado_actual = self.estado
		if estado_actual is not None and hasattr(estado_actual, accion):
			metodo = getattr(estado_actual, accion)
			estado_nuevo = metodo(*args, **kwargs)
			if isinstance(estado_nuevo,tuple):
				return estado_nuevo
			elif estado_nuevo is not None:
				estado_nuevo.save()
		elif estado_actual is None:
			Solicitado(permiso=self, *args, **kwargs).save()
		else:
			raise Exception("Tramite: La accion solicitada no se pudo realizar")

	def agregar_documentacion(self, documento):
		self.documentos.add(documento)

	def falta_entregar_documentacion(self):
			return False if len(self.tipos_de_documentos_faltantes()) == 0 else True

	def falta_visar_documentacion(self):
			return True if self.documentos.filter(estado__lt=2).exists() else False

	def existen_documentos_corregidos(self):
		return True if self.documentos.filter(estado=1).exists() else False

	def documentacion_completa(self):
		return True if ((not self.falta_entregar_documentacion()) and (not self.existen_documentos_corregidos())
				and (not self.falta_visar_documentacion()) and (self.numero_exp != None)) else False

	def tipos_de_documentos_faltantes(self):
		tipos_documentos_requeridos = self.tipo.documentos.all() #DOCUMENTO REQUERIDOS DEL TIPO DE USO
		tipos_documentos_recibidos = [doc.tipo for doc in self.documentos.select_related('tipo')]
		return set(tipos_documentos_requeridos).difference(set(tipos_documentos_recibidos))

	def generar_expediente(self):
		documentos_requeridos = len(self.tipo.documentos.all())-1
		documentos_entregados = len(self.documentos.filter(tipo__protegido=False))
		return True if documentos_entregados >= documentos_requeridos and self.numero_exp == None else False
	
	def montoTotalCobros(self):
		sumaTotalCobros = 0
		for cobro in self.cobros.all():
			sumaTotalCobros +=(cobro.monto)
		return sumaTotalCobros

	def montoTotalPagos(self):
		sumaTotalPagos = 0
		for pago in self.pagos.all():
			sumaTotalPagos +=(pago.monto)
		return sumaTotalPagos

	def saldoActual(self):
		return self.montoTotalPagos() - self.montoTotalCobros()

	def isPermisoFinalizado(self):
			return self.fechaVencimiento < date.today()

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

	def getEstadoString(self):
		return Estado.TIPOS[self.tipo][1]

	def documentos_modificar_eliminar(self):
		return ['acta-de-inspeccion','acta-de-infraccion','cobro-infraccion','pago-infraccion']

	def eliminar_documento(self,usuario, fecha, documento):
		self.permiso.documentos.remove(documento)
		documento.delete()
		return (True,"Se pudo eliminar el {} con exito".format(documento.tipo.nombre))


class Solicitado(Estado):
	TIPO = 1
	utilizando = models.BooleanField(
			help_text="El Solicitante esta utilizando actualmente el recurso hidrico",
			default=False)
	oficio = models.BooleanField(
			help_text="Solicitud de permiso de uso de agua iniciada de oficio por la Inspección",
			default=False)

	def recibir(self, usuario, fecha, documentos):
		for documento in documentos:
			self.permiso.documentos.add(documento)
		return self

	def revisar(self, usuario, fecha, documentos):
		for documento in documentos:
			documento.estado = 2
			documento.save()
		if self.permiso.documentos.filter(estado=2).exists():
			return Visado(permiso=self.permiso, usuario=usuario, fecha_visado=fecha, fecha=fecha) #TODO Establecer fecha de visado como la del documento y fecha como cuando se cargo por sistema
		return self

	def __str__(self):
		return "Solicitado"

	def rechazar(self, usuario, fecha, documentos):
		for documento in documentos:
			documento.estado = 1
			documento.save()
		if self.permiso.documentos.filter(estado=1).exists():
			return Corregido(permiso=self.permiso, usuario=usuario, fecha_corregido=fecha, fecha=fecha) #TODO Establecer fecha de visado como la del documento y fecha como cuando se cargo por sistema
		return self

	def completar(self, usuario, fecha, expediente, pase):
		self.permiso.numero_exp = expediente
		self.permiso.documentos.add(pase)
		self.permiso.save()
		return self

	def documentos_modificar_eliminar(self):
		docs = super().documentos_modificar_eliminar()
		return docs+[doc.slug for doc in self.permiso.tipo.documentos.all()]


class Corregido(Estado):
	TIPO = 2
	fecha_corregido = models.DateField()

	def recibir(self, usuario, fecha, documentos):
		for documento in documentos:
			self.permiso.documentos.add(documento)
		return self

	def rechazar(self, usuario, fecha, documentos):
		for documento in documentos:
			documento.estado = 1
			documento.save()
		return self

	def revisar(self, usuario, fecha, documentos):
		for documento in documentos:
			documento.estado = 2
			documento.save()
		if self.permiso.documentos.filter(estado=1).exists():
			return self
		elif self.permiso.documentacion_completa():
			return Completado(permiso=self.permiso, usuario=usuario, fecha=fecha)
		else:
			return Visado(permiso=self.permiso, usuario=usuario, fecha_visado=fecha, fecha=fecha) #TODO Establecer fecha de visado como la del documento y fecha como cuando se cargo por sistema

	def completar(self, usuario, fecha, expediente, pase):
		self.permiso.numero_exp = expediente
		self.permiso.documentos.add(pase)
		self.permiso.save()
		return self

	def __str__(self):
		return "Corregido"

	def documentos_modificar_eliminar(self):
		docs = super().documentos_modificar_eliminar()
		return docs+[doc.slug for doc in self.permiso.tipo.documentos.all()]
	

class Visado(Estado):
	TIPO = 3
	fecha_visado = models.DateField()

	def __str__(self):
		return "Visado"

	def recibir(self, usuario, fecha, documentos):
		for documento in documentos:
			self.permiso.documentos.add(documento)
		return self

	def revisar(self, usuario, fecha, documentos):
		for documento in documentos:
			documento.estado = 2
			documento.save()
		if self.permiso.documentos.filter(estado=1).exists():
			return Corregido(permiso=self.permiso, usuario=usuario, fecha_corregido=fecha, fecha=fecha) #TODO Establecer fecha de visado como la del documento y fecha como cuando se cargo por sistema
		elif self.permiso.documentacion_completa():
			return Completado(permiso=self.permiso, usuario=usuario, fecha=fecha)
		else:
			return self

	def rechazar(self, usuario, fecha, documentos):
		for documento in documentos:
			documento.estado = 1
			documento.save()
		if self.permiso.documentos.filter(estado=1).exists():
			return Corregido(permiso=self.permiso, usuario=usuario, fecha_corregido=fecha, fecha=fecha) #TODO Establecer fecha de visado como la del documento y fecha como cuando se cargo por sistema
		return self
		
	def completar(self, usuario, fecha, expediente, pase):
		self.permiso.numero_exp = expediente
		self.permiso.documentos.add(pase)
		self.permiso.save()
		if self.permiso.documentacion_completa():
			return Completado(permiso=self.permiso, usuario=usuario, fecha=fecha)
		else:
			return self

	def documentos_modificar_eliminar(self):
		docs = super().documentos_modificar_eliminar()
		return docs+[doc.slug for doc in self.permiso.tipo.documentos.all()]


class Completado(Estado):
	TIPO = 4
	""" Estado del tramite cuando se completo la documentacion del expediente """
	def __str__(self):
		return "Completado"

	def publicar(self, usuario, fecha, tiempo, edicto):
		self.permiso.documentos.add(edicto)
		return Publicado(permiso=self.permiso, usuario=usuario, fecha=fecha, tiempo=tiempo)
	
	def documentos_modificar_eliminar(self):
		docs = super().documentos_modificar_eliminar()
		return docs+['pase']

	def eliminar_documento(self,usuario, fecha, documento):
		if documento.tipo.slug=='pase':
			super().eliminar_documento(usuario, fecha, documento)
			self.permiso.numero_exp = None
			self.permiso.volver_estado_anterior()
			self.permiso.save()
			return (True,"Se pudo eliminar el Pase con exito")
		else:
			super().eliminar_documento(usuario, fecha, documento)
			

class Publicado(Estado):
	TIPO = 5
	# No contemplar dias habiles.... para no entrar en tema de feriados
	tiempo = models.PositiveIntegerField()

	def __str__(self):
		return "Publicado"

	def resolver(self, usuario, fecha, unidad, resolucion, fechaPrimerCobro ,vencimiento):
		if self.fecha + timedelta(days=self.tiempo) < fecha:
			modulos = ValorDeModulo.objects.filter(fecha = fecha, modulo=self.permiso.tipo.tipo_modulo)
			if not modulos.exists():
				raise Exception('No existe el valor de modulo')
			resolucion.save()
			precio = modulos.latest().precio
			monto = self.permiso.tipo.calcular_monto(precio, unidad, fechaPrimerCobro, fecha)
			cobro = Cobro(permiso=self.permiso, documento=resolucion, monto=monto, fecha_desde=fechaPrimerCobro, fecha_hasta=fecha)
			cobro.save()
			self.permiso.unidad = unidad
			self.permiso.fechaVencimiento = vencimiento
			self.permiso.agregar_documentacion(resolucion)
			self.permiso.save()
			return Otorgado(permiso=self.permiso, usuario=usuario, fecha=fecha,fecha_vencimiento=vencimiento)
		return self

	def isEdictoFinalizado(self):
		return self.fecha + timedelta(days=self.tiempo) < date.today()

	def vencimientoPublicacion(self):
		return self.fecha + timedelta(days=self.tiempo)

	def darDeBaja(self, usuario, fecha, oposicion):
		self.permiso.documentos.add(oposicion)
		self.permiso.save()
		return Baja(permiso=self.permiso, usuario=usuario, fecha=fecha)

	def documentos_modificar_eliminar(self):
		docs = super().documentos_modificar_eliminar()
		return docs+['edicto']

	def eliminar_documento(self,usuario, fecha, documento):
		if documento.tipo.slug=='edicto':
			super().eliminar_documento(usuario, fecha, documento)
			self.permiso.volver_estado_anterior()
			return (True,"Se pudo eliminar el Edicto con exito")
		else:
			super().eliminar_documento(usuario, fecha, documento)

class Otorgado(Estado):
	TIPO = 6
	fecha_vencimiento = models.DateField()

	def __str__(self):
		return "Otorgado"

	def cobrar(self, usuario, fecha, monto, pago):
		self.permiso.documentos.add(pago)
		return self

	def recalcular(self, usuario, documento, fecha, unidad):
		cobros = self.permiso.cobros.all()
		
		if not cobros.exists():
			desde = self.permiso.getEstados(1)[0].fecha
			hasta = fecha
		else:
			cobro = cobros.latest()
			desde = cobro.fecha_hasta
			hasta = fecha

		modulos = ValorDeModulo.objects.filter(fecha__lte=hasta, modulo=self.permiso.tipo.tipo_modulo)
		if not modulos.exists():
			raise Exception("con que?")
		precio = modulos.latest().precio
		monto = self.permiso.tipo.calcular_monto(precio, self.permiso.unidad, desde, hasta)

		return Cobro(permiso=self.permiso, documento=documento, monto=monto, fecha_desde=desde, fecha_hasta=hasta)
	
	def renovar(self, usuario, fecha, unidad, resolucion, fechaPrimerCobro ,vencimiento):
		resolucion.save()
		self.permiso.unidad = unidad
		self.permiso.fechaVencimiento = vencimiento
		self.permiso.agregar_documentacion(resolucion)
		self.permiso.save()
		return Otorgado(permiso=self.permiso, usuario=usuario, fecha=fecha,fecha_vencimiento=vencimiento)

	def documentos_modificar_eliminar(self):
		docs = super().documentos_modificar_eliminar()
		return docs+['resolucion']

	def eliminar_documento(self,usuario, fecha, documento):
		if documento.tipo.slug=='resolucion':
			resoluciones = self.permiso.documentos.filter(tipo__slug='resolucion')
			if len(resoluciones)==1:
				cobros=Cobro.objects.filter(permiso=self.permiso)
				if self.permiso.documentos.filter(tipo__slug='pago').exists():
					return (False,"El permiso tiene pagos realizados, no es posible eliminar esta Resolución")
				elif len(cobros)==1:					
					#SI NO TIENE PAGOS DE CANON... ELIMINAR EL PRIMER COBRO, ELIMINAR LA RESOLUCION Y VOLVER AL ESTADO ANTERIOR
					cobros[0].delete()
					documento.delete()
					self.permiso.unidad = None
					self.permiso.fechaVencimiento = None
					self.permiso.volver_estado_anterior()
					self.permiso.save()
					return (True,"Primera Resolución eliminada. El permiso ahora se encuentra en estado de Publicado")
				else:
					return (False,"El permiso tiene dos o más cobros de canon generados, no es posible eliminar esta Resolución")
			else:
				fecha_resolucion = resoluciones.latest('fecha').fecha
				if documento.fecha < fecha_resolucion:
					return (False,"Existen otras resoluciones cargadas, por eso no es posible eliminar este documento")
				if not self.permiso.documentos.filter(tipo__slug='pago',fecha__gte=fecha_resolucion).exists() and not self.permiso.documentos.filter(tipo__slug='cobro',fecha__gte=fecha_resolucion).exists():
					# ELIMINAR LA ULTIMA RESOLUCION, Y VOLVER A LA ULTIMA FECHA DE VENCIMIENTO DE RESOLUCION
					documento.delete()
					self.permiso.volver_estado_anterior()
					self.permiso.fechaVencimiento = self.permiso.estado.fecha_vencimiento
					self.permiso.save()
					return (True,"Ultima resolución eliminada correctamente")
				else:
					return (False,"El permiso tiene generado cobros y/o pagos despues de la fecha de la ultima resolución cargada, no es posible eliminar este documento")
		else:
			super().eliminar_documento(usuario, fecha, documento)

class Baja(Estado):
	TIPO = 7
	def __str__(self):
		return "Baja"

	def documentos_modificar_eliminar(self):
		docs = super().documentos_modificar_eliminar()
		return docs+['resolucion','cobro','pago','oposicion'] #TODO CORROBORAR SI ESTA BIEN


for Klass in Permiso.ESTADOS:
	Estado.register(eval(Klass))

		#valorModulo = ValorDeModulo.objects.filter(fecha='2017-11-13',modulo=1)

		#def calcular_monto(self, modulo, unidad, desde, hasta):
		#dias = (hasta - desde).days
		#horas = dias * 24
		#lapso = horas / self.periodo
		#return self.coeficiente * modulo * unidad * lapso*

		#monto = self.permiso.tipo.calcular_monto(valorModulo, self.permiso.unidad,2017-11-13,2017-11-13)
		#Cobro (permiso=self.permiso, monto=monto, documento=documento, fecha=fecha)