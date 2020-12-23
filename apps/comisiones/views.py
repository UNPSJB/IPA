from django.shortcuts import render
from .forms import *
from apps.documentos.models import Documento
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .models import Comision
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView

from apps.generales.views import GenericListadoView, GenericAltaView

class AltaComision(GenericAltaView):
	model = Comision
	form_class = ComisionForm
	#template_name = 'forms.html'
	template_name = 'comisiones/alta.html'
	success_url = reverse_lazy('comisiones:listar')

	def get_context_data(self, **kwargs):
		context = super(AltaComision, self).get_context_data(**kwargs)
		context['botones'] = {
			'Nuevo Empleado': reverse('personas:alta'),
			'Nueva Localidad': reverse('localidades:alta'),
		}
		context['nombreForm'] = 'Nueva Comisión'
		return context


class DetalleComision(DetailView):
	model = Comision
	template_name = 'comisiones/detalle.html'
	context_object_name = 'comision'

	def get_context_data(self, **kwargs):
		context = super(DetalleComision, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de Comision'
		context['botones'] = {
		'Listado Comisiones': reverse('comisiones:listar'),
		'Modificar Comision': reverse('comisiones:modificar', args=[self.object.id]),
		'Eliminar Comision': reverse('comisiones:eliminar', args=[self.object.id]),
		}
		return context


class ListadoComision(ListView):
	model = Comision
	template_name = 'comisiones/listado.html'
	context_object_name = 'comisiones'

	def get_context_data(self, **kwargs):
		context = super(ListadoComision, self).get_context_data(**kwargs)
		context['nombreReverse'] = 'comisiones'
		context['nombreLista'] = 'Listado de Comisiones'
		context['headers'] = ['Empleados', 'Localidades', 'Fecha Inicio - Fecha Fin', 'Acción', 'Detalle']
		context['botones'] = {'Nueva Comisión': reverse('comisiones:alta')}
		return context

class ModificarComision(UpdateView):
	model = Comision
	form_class = ComisionForm
	template_name = 'comisiones/forms.html'
	success_url = reverse_lazy('comisiones:listar')

	def post(self, request, pk):
		self.object = self.get_object
		id_comision = pk
		comision = self.model.objects.get(id=id_comision)
		form = self.form_class(request.POST, instance=comision)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())
	def get_context_data(self, **kwargs):
		context = super(ModificarComision, self).get_context_data(**kwargs)
		context['botones'] = {
			'Listado Comisiones': reverse('comisiones:listar'),
			'Nuevo Empleado': reverse('personas:alta')
			}
		context['nombreForm'] = 'Nueva Comisión'
		return context


class DeleteComision(DeleteView):
	model = Comision
	template_name = 'delete.html'
	success_url = reverse_lazy('comisiones:listar') 
