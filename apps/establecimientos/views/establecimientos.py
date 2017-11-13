from django.shortcuts import render
from ..forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from ..models import Establecimiento
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView


# Establecimiento
class AltaEstablecimiento(CreateView):
	model = Establecimiento
	form_class = EstablecimientoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('establecimientos:listar')

	def get_context_data(self, **kwargs):
		context = super(AltaEstablecimiento, self).get_context_data(**kwargs)
		context['botones'] = {
			'Listado': reverse('establecimientos:listar'),
			'Nueva persona': reverse('personas:alta'),
			'Nueva localidad': reverse('localidades:alta')
			}
		context['nombreForm'] = 'Nuevo establecimiento'
		return context

class ListadoEstablecimientos(ListView):
	model = Establecimiento
	template_name = 'establecimiento/listado.html'
	context_object_name = 'establecimientos'

	def get_context_data(self, **kwargs):
		context = super(ListadoEstablecimientos, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de establecimientos'
		context['nombreReverse'] = 'establecimientos'
		context['headers'] = ['Nombre', 'Localidad','Código Catastral']
		context['botones'] = {'Alta': reverse('establecimientos:alta')}
		return context

class DetalleEstablecimiento(DetailView):
	model = Establecimiento
	template_name = 'establecimiento/detalle.html'
	context_object_name = 'establecimiento'

	def get_context_data(self, **kwargs):
		context = super(DetalleEstablecimiento, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de establecimiento'
		context['botones'] = {
			'Listado': reverse('establecimientos:listar'),
			'Nuevo establecimiento': reverse('establecimientos:alta'),
			'Eliminar establecimiento': reverse('establecimientos:eliminar', args=[self.object.codigoCatastral])

		}
		return context

class ModificarEstablecimiento(UpdateView):
	model = Establecimiento
	form_class = EstablecimientoForm
	template_name = 'establecimiento/form.html'
	success_url = reverse_lazy('establecimientos:listar')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_establecimiento = kwargs['pk']
		establecimiento = self.mod-el.objects.get(id=id_establecimiento)
		form = self.form_class(request.POST, instance=establecimiento)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())

class DeleteEstablecimiento(DeleteView):
	model = Establecimiento
	template_name = 'establecimiento/delete.html'
	success_url = reverse_lazy('establecimientos:listar')