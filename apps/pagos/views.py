from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from .models import ValorDeModulo, Cobro, Pago
from django.http import HttpResponseRedirect
from .forms import RegistrarValorDeModuloForm, PagoForm
from apps.documentos.forms import DocumentoForm
from django.views.generic import ListView,CreateView,DeleteView
from apps.permisos.models import Permiso
from datetime import date


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
		cobro = permiso.estado().recalcular(request.user, date.today(), permiso.unidad)
		documento_form = DocumentoForm()
		return render(request, self.template_name, {'form':documento_form, 'cobro': cobro, 
			'botones':{'Volver a Permiso': reverse('permisos:detallePermisoOtorgado', args=[permiso.id])},
			'permiso': permiso, 'nombreForm':"Alta Cobro"})

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))

		documento_form = DocumentoForm(request.POST, request.FILES)

		cobro = permiso.estado().recalcular(request.user, date.today(), permiso.unidad)
		
		if documento_form.is_valid():
			documento = documento_form.save()
			cobro.documento = documento
			cobro.permiso = permiso
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
		context['headers'] = ['Periodo', 'Fecha de Cobro', 'Monto($)']
		context['botones'] = {
			'Volver al detalle del permiso':reverse('permisos:detallePermisoOtorgado', args=[self.permiso.pk]),
			}
		return context

class AltaPago(CreateView):
	model = Pago
	form_class = DocumentoForm
	second_form_class = PagoForm
	template_name = 'pagos/alta.html'
	success_url = reverse_lazy('pagos:listarModulos')


	def get_context_data(self, **kwargs):
		context = super(AltaPago, self).get_context_data(**kwargs)
		context['nombreForm'] = "Alta Pago"
		context['headers'] = ['']
		context['botones'] = {
			'Listado':reverse('tipoDocumentos:listar'),
			}
		context['form'] = self.form_class()
		context['form2'] = self.second_form_class()
		return context

	def get(self, request, *args, **kwargs):
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		documento_form = self.form_class()
		pago_form = self.second_form_class()
		return render(request, self.template_name, {'form':documento_form,'form2':pago_form, 
			'botones':{'Volver a Permiso': reverse('permisos:detallePermisoOtorgado', args=[permiso.id])},
			'permiso': permiso, 'nombreForm':"Alta Pago"})

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		permiso = Permiso.objects.get(pk=kwargs.get('pk'))

		documento_form = DocumentoForm(request.POST, request.FILES)
		pago_form = PagoForm(request.POST)
		
		if documento_form.is_valid() and pago_form.is_valid():
			documento = documento_form.save()
			pago = pago_form.save(commit=False)
			pago.documento = documento
			pago.permiso = permiso
			pago.fecha = pago_form.data['fecha']
			pago.monto = pago_form.data['fecha']
			print(pago)
			print(pago)
			print(pago)
			raise Exception
			pago.save()
			return HttpResponseRedirect(reverse('permisos:detallePermisoOtorgado', args=[permiso.id]))
		return render(request, self.template_name, {'form':documento_form,'form2':pago_form, 'botones':'', 'permiso': permiso})