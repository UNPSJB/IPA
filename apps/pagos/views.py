from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from .models import ValorDeModulo, Cobro, Pago
from django.http import HttpResponseRedirect
from .forms import RegistrarValorDeModuloForm
from apps.documentos.forms import DocumentoForm
from django.views.generic import ListView,CreateView,DeleteView
from apps.permisos.models import Permiso
from datetime import date, datetime

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
			'Salir': reverse('index')
			}
		return context

class EliminarValorDeModulo(DeleteView):
	model = ValorDeModulo
	template_name = 'delete.html'
	success_url = reverse_lazy('pagos:listarModulos')

class AltaCobro(CreateView):
	model = Cobro
	template_name = 'cobros/detalle.html'
	success_url = reverse_lazy('pagos:listarModulos')

	def get_context_data(self, **kwargs):
		context = super(AltaCobro, self).get_context_data(**kwargs)
		context['nombreForm'] = "Alta Cobro"
		context['headers'] = ['']
		context['botones'] = {
			'Listado':reverse('tipoDocumentos:listar'),
			}
		return context

	def get(self, request, *args, **kwargs):
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		documento_form = DocumentoForm()
		cobro = permiso.estado().recalcular(usuario=request.user, documento=None, fecha=date.today(), unidad=permiso.unidad)
		return render(request, self.template_name, {'form':documento_form, 'cobro': cobro, 
			'botones':{'Volver a Permiso': reverse('permisos:detallePermisoOtorgado', args=[permiso.id])},
			'permiso': permiso, 'nombreForm':"Alta Cobro"})

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))

		documento_form = DocumentoForm(request.POST, request.FILES)

		if documento_form.is_valid():
			documento = documento_form.save()
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
		return self.permiso.cobros.all()

	def get_context_data(self, **kwargs):
		context = super(ListarCobros, self).get_context_data(**kwargs)
		context['nombreForm'] = "Listado de Cobros"
		context['headers'] = ['Periodo', 'Fecha de Cobro', 'Monto($)', 'Documento de Cobro']
		context['botones'] = {
			'Volver al detalle del permiso':reverse('permisos:detallePermisoOtorgado', args=[self.permiso.pk]),
			}
		return context

class AltaPago(CreateView):
	model = Pago
	form_class = DocumentoForm
	template_name = 'pagos/alta.html'

	def get_success_url(self):
		return reverse('permisos:detallePermisoOtorgado', args=(self.permiso_pk, ))

	def get_context_data(self, **kwargs):
		context = super(AltaPago, self).get_context_data(**kwargs)
		context['nombreForm'] = "Alta Pago"
		context['headers'] = ['']
		context['botones'] = {
			'Listado':reverse('tipoDocumentos:listar'),
			}
		context['form'] = self.form_class()
		return context

	def get(self, request, *args, **kwargs):
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		documento_form = self.form_class()
		documento_form.fields['fecha'].label = 'Fecha de Pago'
		return render(request, self.template_name, {'form':documento_form, 
			'botones':{'Volver a Permiso': reverse('permisos:detallePermisoOtorgado', args=[permiso.id])},
			'permiso': permiso, 'nombreForm':"Alta Pago"})

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))

		documento_form = DocumentoForm(request.POST, request.FILES)
		documentos = permiso.documentos.all()

		monto = float(request.POST['monto'])
		fecha_de_pago = datetime.strptime(documento_form.data['fecha'], "%Y-%m-%d").date()
		lista_resoluciones = [doc for doc in documentos if (doc.tipo.nombre == 'Resolucion')] #FIXME: VA TIPO DEFINIDO PARA PASE
		fecha_primer_resolucion = lista_resoluciones[0].fecha

		if documento_form.is_valid():
			if (monto > 0) and (fecha_de_pago > fecha_primer_resolucion) and (fecha_de_pago <= date.today()):
				raise Exception
				documento = documento_form.save()
				pago = Pago(permiso=permiso, monto=monto, documento=documento, fecha=fecha_de_pago)
				pago.save()
				return HttpResponseRedirect(self.get_success_url())
			else:
				return self.render_to_response(self.get_context_data(form=documento_form, permiso=permiso, message = 'La fecha de Pago debe ser mayor o igual a la fecha de de la resolución de otorgamiento de permiso y menor o igual a la fecha actual ('
				+ (fecha_primer_resolucion).strftime("%d-%m-%Y") + ' - ' + (date.today()).strftime("%d-%m-%Y") + ')'))
		raise Exception
		return self.render_to_response(self.get_context_data(form=documento_form, permiso=permiso))

class ListarPagos(ListView):
	model = Pago
	template_name = 'pagos/listado.html'
	context_object_name = 'pagos'

	def get(self, request, *args, **kwargs):
		self.permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		return super(ListarPagos,self).get(request, *args, **kwargs)

	def get_queryset(self):
		return self.permiso.pagos.all()

	def get_context_data(self, **kwargs):
		context = super(ListarPagos, self).get_context_data(**kwargs)
		context['nombreForm'] = "Listado de Pagos"
		context['headers'] = ['Fecha de Pago', 'Monto($)', 'Documento de Pago']
		context['botones'] = {
			'Volver al detalle del permiso':reverse('permisos:detallePermisoOtorgado', args=[self.permiso.pk]),
			}
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