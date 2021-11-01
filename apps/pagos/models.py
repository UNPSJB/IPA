from django.db import models
from apps.documentos.models import Documento
from django.db.models import FloatField
from django.db.models import Sum, F
from django.db.models import Q

class OperacionManager(models.Manager):
	def ingresos(self,data,fecha_desde,fecha_hasta,serie_temporal):
		operaciones_filters = Q()
		operaciones_filters &= Q(permiso__tipo__pk__in= data['tipos_permisos']) if data['tipos_permisos'].exists() else Q()
		operaciones_filters &= Q(es_por_canon=data['motivos']) if data['motivos'] !='' else Q()
		operaciones_filters &= Q(fecha__range=[fecha_desde, fecha_hasta])
		if serie_temporal:
			return self.get_queryset().filter(operaciones_filters).annotate(tipo=F('permiso__tipo__descripcion'),motivo=F('es_por_canon')).values(
				'fecha','tipo','motivo').annotate(monto=Sum(F('monto'),output_field=FloatField())).order_by('fecha')
			#values(fecha='fecha',tipo='permiso__tipo__descripcion',motivo='es_por_canon').annotate(monto=Sum(F('monto'),output_field=FloatField())).order_by('fecha')
		else:
			operaciones_filters &= Q(permiso__afluente__pk__in=data['afluentes']) if data['afluentes'].exists() else Q()
			operaciones_filters &= Q(permiso__establecimiento__localidad__pk__in=data['localidades']) if data['localidades'].exists() else Q()
			operaciones_filters &= Q(permiso__establecimiento__localidad__departamento__pk__in=data['departamentos']) if data['departamentos'].exists() else Q()
			return self.get_queryset().filter(operaciones_filters).values('permiso__tipo__descripcion','es_por_canon').annotate(monto=Sum(F('monto'),output_field=FloatField()))

class Operacion(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True)
	monto = models.DecimalField(max_digits = 10, decimal_places = 2)
	documento = models.ForeignKey(Documento, blank=False, null=False)
	fecha = models.DateField()
	es_por_canon = models.BooleanField(default=True)
	operaciones = OperacionManager()

	def tipo_de_pago(self):
		return "Canon" if self.es_por_canon else "Infraccion"

	
		
class Pago(Operacion):
	permiso = models.ForeignKey('permisos.Permiso', blank=False, null=False, related_name="pagos")

	@classmethod
	def getPagosCanon(Klass):
		return Pago.objects.all().filter(es_por_canon=True)

	@classmethod
	def getPagosInfraccion(Klass):
		return Pago.objects.all().filter(es_por_canon=False)


class Cobro(Operacion):
	permiso = models.ForeignKey('permisos.Permiso', blank=False, null=False, related_name="cobros")
	fecha_desde = models.DateField()

	class Meta:
		get_latest_by = "fecha"

	@classmethod
	def getCobrosCanon(Klass):
		return Cobro.objects.all().filter(es_por_canon=True)

	@classmethod
	def getCobrosInfraccion(Klass):
		return Cobro.objects.all().filter(es_por_canon=False)

# MODULOS ===================================================
class ValorDeModulo (models.Model):
	DIESEL = 1
	KW = 2
	TipoModulo = [
		(DIESEL, 'Diesel'),
		(KW, 'Kw')
	]
	
	modulo = models.PositiveIntegerField(choices=TipoModulo)
	precio = models.DecimalField(max_digits = 10, decimal_places = 2)
	fecha = models.DateField()
	descripcion = models.TextField()

	class Meta:
		ordering = ["fecha"]
		unique_together = ("fecha", "modulo")
		get_latest_by = "fecha"

	def __str__(self):
		return "{fecha}: ${precio}".format(fecha=self.fecha, precio=self.precio)
