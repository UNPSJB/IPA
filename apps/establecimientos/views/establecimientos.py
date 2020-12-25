from django.shortcuts import render
from ..forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from ..models import Establecimiento
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView

from apps.generales.views import GenericAltaView, GenericListadoView
from ..tables import EstablecimientosTable
from ..filters import EstablecimientosFilter

# Establecimiento
class AltaEstablecimiento(CreateView):
	model = Establecimiento
	form_class = EstablecimientoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('establecimientos:listar')

	def get_context_data(self, **kwargs):
		context = super(AltaEstablecimiento, self).get_context_data(**kwargs)
		context['botones'] = {
			'Ir a Listado': reverse('establecimientos:listar'),
			'Nuevo Solicitante': reverse('personas:alta')
			}
		context['nombreForm'] = 'Nuevo Establecimiento'
		return context

class ListadoEstablecimientos(GenericListadoView):
	model = Establecimiento
	template_name = 'establecimientos/listado.html'
	table_class = EstablecimientosTable
	paginate_by = 20
	filterset_class = EstablecimientosFilter
	context_object_name = 'establecimientos'

	def get_context_data(self, **kwargs):
		context = super(ListadoEstablecimientos, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de Establecimientos'
		context['nombreReverse'] = 'establecimientos'
		context['headers'] = ['Nombre', 'Localidad','Código Catastral']
		context['botones'] = {
		}	
		return context

class DetalleEstablecimiento(DetailView):
	model = Establecimiento
	template_name = 'establecimientos/detalle.html'
	context_object_name = 'establecimiento'

	def get_context_data(self, **kwargs):
		context = super(DetalleEstablecimiento, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de Establecimiento'
		context['botones'] = {
			'Ir a Listado': reverse('establecimientos:listar'),
			'Nuevo Establecimiento': reverse('establecimientos:alta'),
			'Modificar Establecimiento': reverse('establecimientos:modificar', args=[self.object.codigoCatastral]),
			'Eliminar Establecimiento': reverse('establecimientos:eliminar', args=[self.object.codigoCatastral]),
		}
		return context

class ModificarEstablecimiento(UpdateView):
	model = Establecimiento
	form_class = EstablecimientoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('establecimientos:listar')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_establecimiento = kwargs['pk']
		establecimiento = self.model.objects.get(codigoCatastral=id_establecimiento)
		form = self.form_class(request.POST, instance=establecimiento)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		context = super(ModificarEstablecimiento, self).get_context_data(**kwargs)
		context['nombreForm'] = "Modificar Establecimiento"
		context['botones'] = {
			'Ir a Listado': reverse('establecimientos:listar')
			}
		return context


class DeleteEstablecimiento(DeleteView):
	model = Establecimiento
	template_name = 'delete.html'
	success_url = reverse_lazy('establecimientos:listar')