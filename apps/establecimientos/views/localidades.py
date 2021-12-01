from django.shortcuts import render
from ..forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from ..models import Localidad
from django.views.generic import ListView,CreateView,DetailView,DeleteView,UpdateView

from apps.generales.views import GenericAltaView, GenericListadoView
from ..tables import LocalidadesTable
from ..filters import LocalidadesFilter

#Localidad

class AltaLocalidad(GenericAltaView):
	model = Localidad
	form_class = LocalidadForm
	template_name = 'establecimientos/localidades/alta.html'
	success_url = reverse_lazy('localidades:listar')

	def get_context_data(self, **kwargs):
		context = super(AltaLocalidad, self).get_context_data(**kwargs) 
		context['nombreForm'] = 'Nueva Localidad'
		context['ayuda'] = 'localidad.html#como-crear-una-nueva-localidad'
		return context

class ModificarLocalidad(UpdateView):
	model = Localidad
	form_class = LocalidadForm
	template_name = 'establecimientos/localidades/alta.html'
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
		context['return_path'] = reverse('localidades:listar')
		return context


class ListadoLocalidades(GenericListadoView):
	model = Localidad
	template_name = 'establecimientos/localidades/listado.html'
	table_class = LocalidadesTable
	paginate_by = 20
	filterset_class = LocalidadesFilter
	export_name = 'listado_localidades'

	def get_context_data(self, **kwargs):
		context = super(ListadoLocalidades, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de Localidades'
		context['nombreReverse'] = 'localidades'
		context['headers'] = ['Código Postal', 'Nombre','Departamento']
		context['botones'] = {'Nueva Localidad': reverse('localidades:alta')}
		return context

class LocalidadDelete(DeleteView):
	model = Localidad
	template_name = 'delete.html'
	success_url = reverse_lazy('localidades:listar') 