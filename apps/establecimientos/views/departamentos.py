from django.shortcuts import render
from ..forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from ..models import Departamento
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView


#Departamento

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

class ListadoDepartamentos(ListView):
	model = Departamento
	template_name = 'departamento/listado.html'
	context_object_name = 'departamentos'

	def get_context_data(self, **kwargs):
		context = super(ListadoDepartamentos, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de Departamentos'
		context['nombreReverse'] = 'departamentos'
		context['headers'] = ['Nombre','Población']
		context['botones'] = {
				
			}
		return context




