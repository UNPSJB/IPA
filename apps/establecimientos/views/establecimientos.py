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
class AltaEstablecimiento(GenericAltaView):
	model = Establecimiento
	form_class = EstablecimientoForm
	template_name = 'establecimientos/alta.html'
	success_url = reverse_lazy('establecimientos:listar')

	def get_context_data(self, **kwargs):
		context = super(AltaEstablecimiento, self).get_context_data(**kwargs)
		context['botones'] = {
			'Nuevo Solicitante': reverse('personas:alta'),
			}
		context['nombreForm'] = "Nuevo Establecimiento"
		context['ayuda'] = 'solicitante.html#como-crear-un-nuevo-establecimiento'
		if context['return_label'] == None:
			context['return_label'] = "listado de Establecimientos"
		return context

class ListadoEstablecimientos(GenericListadoView):
	model = Establecimiento
	template_name = 'establecimientos/listado.html'
	table_class = EstablecimientosTable
	paginate_by = 20
	filterset_class = EstablecimientosFilter
	context_object_name = 'establecimientos'
	export_name = 'listado_establecimientos'

	def get_context_data(self, **kwargs):
		context = super(ListadoEstablecimientos, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de Establecimientos'
		return context

class DetalleEstablecimiento(DetailView):
	model = Establecimiento
	template_name = 'establecimientos/detalle.html'
	context_object_name = 'establecimiento'

	def get_context_data(self, **kwargs):
		context = super(DetalleEstablecimiento, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de Establecimiento'
		context['botones'] = {
			'Nuevo Establecimiento': reverse('establecimientos:alta'),
			'Modificar Establecimiento': reverse('establecimientos:modificar', args=[self.object.codigoCatastral]),
			'Eliminar Establecimiento': reverse('establecimientos:eliminar', args=[self.object.codigoCatastral]),
		}
		context['return_label'] = 'listado de Establecimientos'
		context['return_path'] = reverse('establecimientos:listar')
		return context

class ModificarEstablecimiento(UpdateView):
	model = Establecimiento
	form_class = EstablecimientoForm
	template_name = 'establecimientos/alta.html'
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
		context['return_path'] = reverse('establecimientos:listar')
		return context


class DeleteEstablecimiento(DeleteView):
	model = Establecimiento
	template_name = 'delete.html'
	success_url = reverse_lazy('establecimientos:listar')