from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from .models import ValorDeModulo, Cobro, Pago
from django.http import HttpResponseRedirect
from .forms import RegistrarValorDeModuloForm
from apps.documentos.forms import DocumentoForm, DocumentoProtegidoForm
from django.views.generic import ListView,CreateView,DeleteView
from apps.permisos.models import Permiso
from datetime import date, datetime
from apps.documentos.models import TipoDocumento
from django.shortcuts import redirect

class AltaValorDeModulo(CreateView):
	model = ValorDeModulo
	form_class = RegistrarValorDeModuloForm
	template_name = 'forms.html'
	success_url = reverse_lazy('pagos:listarModulos')

	def get_context_data(self, **kwargs):
		context = super(AltaValorDeModulo, self).get_context_data(**kwargs)
		context['nombreForm'] = "Alta Valor de Modulo"
		context['headers'] = ['']
		context['botones'] = {
			'Listado':reverse('tipoDocumentos:listar'),
			}
		return context

class ListadoValoresDeModulo(ListView):
	model = ValorDeModulo
	template_name = 'modulos/listado.html'
	context_object_name = 'modulos'

	def get_context_data(self, **kwargs):
		context = super(ListadoValoresDeModulo, self).get_context_data(**kwargs)
		context['nombreLista'] = "Listado de tipos de documento"
		context['headers'] = ['Precio', 'Fecha', 'Descripcion', 'Detalle']
		context['botones'] = {
			'Alta Valor de Modulo': reverse('pagos:altaModulo'),
			}
		return context

class EliminarValorDeModulo(DeleteView):
	model = ValorDeModulo
	template_name = 'delete.html'
	success_url = reverse_lazy('pagos:listarModulos')

class AltaCobro(CreateView):
	model = Cobro
	form_class = DocumentoProtegidoForm
	template_name = 'cobros/detalle.html'
	success_url = reverse_lazy('pagos:listarModulos')

	def get_context_data(self, **kwargs):
		context = super(AltaCobro, self).get_context_data(**kwargs)
		context['nombreForm'] = "Nuevo Cobro de Canon"
		context['headers'] = ['']
		context['botones'] = {
			'Listado':reverse('tipoDocumentos:listar'),
			}
		return context

	def get(self, request, *args, **kwargs):
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		cobro = permiso.estado().recalcular(usuario=request.user, documento=None, fecha=date.today(), unidad=permiso.unidad)
		return render(request, self.template_name, {'form':self.form_class(), 'cobro': cobro, 
			'botones':{'Volver a Permiso': reverse('permisos:detallePermisoOtorgado', args=[permiso.id])},
			'permiso': permiso, 'nombreForm':"Nuevo Cobro de Canon"})

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		documento_form = self.form_class(request.POST, request.FILES)

		if documento_form.is_valid():
			documento = documento_form.save(commit=False)
			documento.tipo = TipoDocumento.get_protegido('cobro')
			documento.visado = True
			documento.save()
			cobro = permiso.estado().recalcular(request.user, documento, date.today(), permiso.unidad)
			cobro.save()

			return HttpResponseRedirect(reverse('permisos:detallePermisoOtorgado', args=[permiso.id]))
		return render(request, self.template_name, {'form':documento_form, 'cobro': cobro, 'botones':'', 'permiso': permiso})


class ListarCobros(ListView):
	model = Cobro
	template_name = 'cobros/listado.html'
	context_object_name = 'cobros'

	def get(self, request, *args, **kwargs):
		self.permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		return super(ListarCobros,self).get(request, *args, **kwargs)

	def get_queryset(self):
		return Cobro.getCobrosCanon().union(Cobro.getCobrosInfraccion())

	def get_context_data(self, **kwargs):
		context = super(ListarCobros, self).get_context_data(**kwargs)
		context['nombreForm'] = "Listado de Cobros"
		context['headers'] = ['Periodo', 'Fecha de Cobro', 'Monto($)', 'Documento de Cobro']
		context['botones'] = {
			'Volver al detalle del permiso':reverse('permisos:detallePermisoOtorgado', args=[self.permiso.pk]),
			}
		context['cobrosCanon'] = Cobro.getCobrosCanon()
		context['cobrosInfraccion'] = Cobro.getCobrosInfraccion()
		return context

class AltaPago(CreateView):
	model = Pago
	form_class = DocumentoProtegidoForm
	template_name = 'pagos/alta.html'

	def get_context_data(self, **kwargs):
		context = super(AltaPago, self).get_context_data(**kwargs)
		context['nombreForm'] = "Nuevo Pago"
		context['headers'] = ['']
		context['botones'] = {
			'Listado':reverse('tipoDocumentos:listar'),
			}
		context['form'] = self.form_class()
		return context

	def get(self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		documento_form = self.form_class()
		documento_form.fields['fecha'].label = 'Fecha de Pago'
		return render(request, self.template_name, {'form':documento_form, 
			'botones':{'Volver a Permiso': reverse('permisos:detallePermisoOtorgado', args=[permiso.id])},
			'permiso': permiso, 'nombreForm':"Nuevo Pago"})

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))

		documento_form = self.form_class(request.POST, request.FILES)
		documentos = permiso.documentos.all()

		monto = float(request.POST['monto'])
		fecha_de_pago = datetime.strptime(documento_form.data['fecha'], "%Y-%m-%d").date()
		lista_resoluciones = [doc for doc in documentos if (doc.tipo.nombre == 'Resolución')] #FIXME: VA TIPO DEFINIDO PARA PASE
		fecha_primer_resolucion = lista_resoluciones[0].fecha

		if documento_form.is_valid():
			if (monto > 0) and (fecha_de_pago > fecha_primer_resolucion) and (fecha_de_pago <= date.today()):
				documento = documento_form.save(commit=False)
				documento.tipo = TipoDocumento.get_protegido('pago')
				documento.visado = True
				documento.save()
				pago = Pago(permiso=permiso, monto=monto, documento=documento, fecha=fecha_de_pago)
				pago.save()
				return HttpResponseRedirect(reverse('permisos:detallePermisoOtorgado', args=[permiso.id,]))
			else:
				return self.render_to_response(self.get_context_data(form=documento_form, permiso=permiso, message = 'La fecha de Pago debe ser mayor o igual a la fecha de de la resolución de otorgamiento de permiso y menor o igual a la fecha actual ('
				+ (fecha_primer_resolucion).strftime("%d-%m-%Y") + ' - ' + (date.today()).strftime("%d-%m-%Y") + ')'))
		return self.render_to_response(self.get_context_data(form=documento_form, permiso=permiso))

class ListarPagos(ListView):
	model = Pago
	template_name = 'pagos/listado.html'
	context_object_name = 'pagos'

	def get(self, request, *args, **kwargs):
		self.permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		return super(ListarPagos,self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ListarPagos, self).get_context_data(**kwargs)
		context['nombreForm'] = "Listado de Pagos"
		context['headers'] = ['Fecha de Pago', 'Monto($)', 'Documento de Pago']
		context['botones'] = {
			'Volver al detalle del permiso':reverse('permisos:detallePermisoOtorgado', args=[self.permiso.pk]),
			}
		context['pagosCanon'] = Pago.getPagosCanon()
		context['pagosInfraccion'] = Pago.getPagosInfraccion()
		return context


class ListarTodosLosCobros(ListView):
	model = Cobro
	template_name = 'cobros/listado.html'
	context_object_name = 'cobros'

	def get_context_data(self, **kwargs):
		context = super(ListarTodosLosCobros, self).get_context_data(**kwargs)
		context['nombreForm'] = "Listado de Cobros Generales"
		context['headers'] = ['Periodo', 'Fecha de Cobro', 'Monto($)', 'Documento de Cobro']
		context['botones'] = {
			}
		return context

class ListarTodosLosPagos(ListView):
	model = Pago
	template_name = 'pagos/listado.html'
	context_object_name = 'pagos'

	def get_context_data(self, **kwargs):
		context = super(ListarTodosLosPagos, self).get_context_data(**kwargs)
		context['nombreForm'] = "Listado de Pagos Generales"
		context['headers'] = ['Fecha de Pago', 'Monto($)', 'Documento de Pago']
		context['botones'] = {
			}
		return context


class AltaCobroInfraccion(CreateView):
	model = Cobro
	form_class = DocumentoProtegidoForm
	template_name = 'cobros/infraccion/alta.html'


	def get_context_data(self, **kwargs):
		context = super(AltaCobroInfraccion, self).get_context_data(**kwargs)
		context['nombreForm'] = "Nuevo Cobro de Infraccion"
		context['headers'] = ['']
		context['botones'] = {
		'Volver a Detalle de Solicitud': reverse('solicitudes:detalle', args=[self.permiso_pk])
		}
		context['permiso'] = Permiso.objects.get(pk=self.permiso_pk)
		return context


	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		return super(AltaCobroInfraccion, self).get(request,*args,**kwargs)	


	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))

		documento_form = DocumentoProtegidoForm(request.POST, request.FILES)
		documento = documento_form.save(commit=False)
		fecha_de_cobro = documento.fecha
		monto = float(request.POST['monto'])

		if documento_form.is_valid():
			if fecha_de_cobro >= permiso.fechaSolicitud:

				documento.tipo = TipoDocumento.get_protegido('cobro-infraccion')
				documento.visado = True
				documento = documento_form.save()
				cobro = Cobro(permiso=permiso, monto=monto, documento=documento, 
					fecha_desde=fecha_de_cobro, fecha_hasta=fecha_de_cobro, es_por_canon=False)
				cobro.save()
				return HttpResponseRedirect(reverse('permisos:detallePermisoOtorgado', args=[permiso.pk,]))
			else:
				return render(request, self.template_name, {'form': documento_form, 'permiso':permiso, 'botones':'', 'nombreForm': 'Nuevo Cobro de Infraccion',
					'message_error': 'La fecha de cobro debe ser igual o mayor a la fecha de solicitud (' + permiso.fechaSolicitud.strftime('%d/%m/%Y'+')')
					})
		return render(request, self.template_name, {'form':documento_form, 'permiso': permiso, 'botones':''})


class AltaPagoInfraccion(CreateView):
	model = Pago
	form_class = DocumentoProtegidoForm
	template_name = 'pagos/infraccion.html'

	def get_context_data(self, **kwargs):
		context = super(AltaPagoInfraccion, self).get_context_data(**kwargs)
		context['nombreForm'] = "Nuevo Pago de Infraccion"
		context['headers'] = ['']
		context['botones'] = {
			'Listado':reverse('tipoDocumentos:listar'),
			}
		context['form'] = self.form_class()
		return context

	def get(self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		documento_form = self.form_class()
		documento_form.fields['fecha'].label = 'Fecha de Pago'
		return render(request, self.template_name, {'form':documento_form, 
			'botones':{'Volver a Permiso': reverse('permisos:detallePermisoOtorgado', args=[permiso.id])},
			'permiso': permiso, 'nombreForm':"Nuevo Pago de Infraccion"})

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))

		documento_form = self.form_class(request.POST, request.FILES)

		monto = float(request.POST['monto'])
		fecha_de_pago = datetime.strptime(documento_form.data['fecha'], "%Y-%m-%d").date()
		fechaSolicitud = permiso.fechaSolicitud

		if documento_form.is_valid():
			if (monto > 0) and (fecha_de_pago >= fechaSolicitud) and (fecha_de_pago <= date.today()):
				documento = documento_form.save(commit=False)
				documento.tipo = TipoDocumento.get_protegido('pago-infraccion')
				documento.visado = True
				documento.save()
				pago = Pago(permiso=permiso, monto=monto, documento=documento, fecha=fecha_de_pago, es_por_canon=False)
				pago.save()
				return HttpResponseRedirect(reverse('permisos:detallePermisoOtorgado', args=[permiso.id,]))
			else:
				return self.render_to_response(self.get_context_data(form=documento_form, permiso=permiso, message = 'La fecha de Pago debe ser mayor o igual a la fecha de Solicitud de permiso y menor o igual a la fecha actual ('
				+ (fechaSolicitud).strftime("%d-%m-%Y") + ' - ' + (date.today()).strftime("%d-%m-%Y") + ')'))
		return self.render_to_response(self.get_context_data(form=documento_form, permiso=permiso))