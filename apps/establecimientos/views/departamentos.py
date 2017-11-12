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
	success_url = reverse_lazy('departamento:listar')

	def get_context_data(self, **kwargs):
		context = super(AltaDepartamento, self).get_context_data(**kwargs)
		context['botones'] = {
				'Listado': reverse('departamentos:listar')
			}
		context['nombreForm'] = 'Nuevo departamento'
		return context

class DetalleDepartamento(DetailView):
	model = Departamento
	template_name = 'departamentos/detalle.html'		

class ListadoDepartamentos(ListView):
	model = Departamento
	template_name = 'departamento/listado.html'
	context_object_name = 'establecimientos'

	def get_context_data(self, **kwargs):
		context = super(ListadoDepartamentos, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de departamentos'
		context['headers'] = ['Nombre','Poblacion']
		context['botones'] = {
				'Alta': reverse('establecimientos:altaDepartamento')
			}
		return context

class ModificarDepartamento(UpdateView):
	model = Departamento
	form_class = DepartamentoForm
	template_name = 'departamentos/form.html'
	success_url = reverse_lazy('departamento:listar')

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
	template_name = 'departamentos/delete.html'
	success_url = reverse_lazy('departamentos:listar')