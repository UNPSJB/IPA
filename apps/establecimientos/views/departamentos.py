from django.shortcuts import render
from ..forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from ..models import Departamento
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView


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
		context['nombreForm'] = 'Nuevo departamento'
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
			'Nuevo Departamento': reverse('departamentos:alta'),
			'Eliminar Departamento': reverse('departamentos:eliminar', args=[self.object.id])
		}
		return context

class ListadoDepartamentos(ListView):
	model = Departamento
	template_name = 'departamento/listado.html'
	context_object_name = 'departamentos'

	def get_context_data(self, **kwargs):
		context = super(ListadoDepartamentos, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de departamentos'
		context['nombreReverse'] = 'departamentos'
		context['headers'] = ['Nombre','Poblacion']
		context['botones'] = {
				'Nuevo departamento': reverse('departamentos:alta')
			}
		return context

class ModificarDepartamento(UpdateView):
	model = Departamento
	form_class = DepartamentoForm
	template_name = 'departamentos/form.html'
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

class DeleteDepartamento(DeleteView):
	model = Departamento
	template_name = 'delete.html'
	success_url = reverse_lazy('departamentos:listar')
