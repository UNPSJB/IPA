from django.shortcuts import render
from ..forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from ..models import Departamento
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView

from apps.generales.views import GenericListadoView, GenericAltaView
from ..tables import DepartamentosTable
from ..filters import DepartamentosFilter
#Departamento

class AltaDepartamento(CreateView):
	model = Departamento
	form_class = DepartamentoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('departamentos:listar')

	def get_context_data(self, **kwargs):
		context = super(AltaDepartamento, self).get_context_data(**kwargs)
		context['botones'] = {
				'Listado': reverse('departamentos:listar')

			}
		context['nombreForm'] = 'Nuevo Departamento'
		return context

class ModificarDepartamento(UpdateView):
	model = Departamento
	form_class = DepartamentoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('departamentos:listar')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_departamento = kwargs['pk']
		departamento = self.model.objects.get(id=id_departamento)
		form = self.form_class(request.POST, instance=departamento)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		context = super(ModificarDepartamento, self).get_context_data(**kwargs)
		context['nombreForm'] = "Modificar Departamento"
		context['botones'] = {
			'Listado': reverse('departamentos:listar')
			}
		return context

class DetalleDepartamento(DetailView):
	model = Departamento
	template_name = 'departamento/detalle.html'		
	context_object_name = 'departamento'

	def get_context_data(self, **kwargs):
		context = super(DetalleDepartamento, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de Departamento'
		context['botones'] = {
			'Listado': reverse('departamentos:listar'),
		}
		return context

class ListadoDepartamentos(GenericListadoView):
	model = Departamento
	#template_name = 'departamento/listado.html'
	
	template_name = 'generales/listado.html'
	table_class = DepartamentosTable
	paginate_by = 12
	filterset_class = DepartamentosFilter
	
	context_object_name = 'departamentos'

	def get_context_data(self, **kwargs):
		context = super(ListadoDepartamentos, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de Departamentos'
		context['nombreReverse'] = 'departamentos'
		context['headers'] = ['Nombre','Población']
		context['botones'] = {
				
			}
		
		return context

class DeleteDepartamento(DeleteView):
	model = Departamento
	template_name = 'delete.html'
	success_url = reverse_lazy('departamentos:listar')


