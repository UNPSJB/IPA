from django.shortcuts import render
from ..forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from ..models import Localidad
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView

#Localidad
class AltaLocalidad(CreateView):
	model = Localidad
	form_class = LocalidadForm
	template_name = 'forms.html'
	success_url = reverse_lazy('localidades:listar')

	def get_context_data(self, **kwargs):
		context = super(AltaLocalidad, self).get_context_data(**kwargs)
		context['botones'] = {
			'Ir a Listado': reverse('localidades:listar'),
			'Nuevo Departamento': reverse('departamentos:alta'),
		}
		context['nombreForm'] = 'Nueva Localidad'
		return context

class DetalleLocalidad(DetailView):
	model = Localidad
	template_name = 'localidad/detalle.html'
	context_object_name = 'localidad'
	
	def get_context_data(self, **kwargs):
		context = super(DetalleLocalidad, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de Localidad'
		context['botones'] = {
			'Ir a Listado': reverse('localidades:listar'),
			'Nueva Localidad': reverse('localidades:alta'),
			'Modificar Localidad': reverse('localidades:modificar', args=[self.object.id]),
			'Eliminar Localidad': reverse('localidades:eliminar', args=[self.object.id]),
		}
		return context

class ListadoLocalidades(ListView):
	model = Localidad
	template_name = 'localidad/listado.html'
	context_object_name = 'localidades'

	def get_context_data(self, **kwargs):
		context = super(ListadoLocalidades, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de Localidades'
		context['nombreReverse'] = 'localidades'
		context['headers'] = ['Código Postal', 'Nombre','Departamento']
		context['botones'] = {
			'Nueva Localidad': reverse('localidades:alta'),
			'Ir a Establecimientos': reverse('establecimientos:listar'),
			'Ir a Afluentes': reverse('afluentes:listar')
			}
		return context

class ModificarLocalidad(UpdateView):
	model = Localidad
	form_class = LocalidadForm
	template_name = 'forms.html'
	success_url = reverse_lazy('localidades:listar')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_localidad = kwargs['pk']
		localidad = self.model.objects.get(id=id_localidad)
		form = self.form_class(request.POST, instance=localidad)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		context = super(ModificarLocalidad, self).get_context_data(**kwargs)
		context['nombreForm'] = "Modificar Localidad"
		context['botones'] = {
			'Ir a Listado': reverse('localidades:listar'),
			'Nuevo Departamento': reverse('departamentos:alta')
			}
		return context

class LocalidadDelete(DeleteView):
	model = Localidad
	template_name = 'delete.html'
	success_url = reverse_lazy('localidades:listar')