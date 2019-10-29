from django.shortcuts import render
from ..forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from ..models import Localidad
from django.views.generic import ListView,CreateView,DetailView,DeleteView,UpdateView

#Localidad


class DetalleLocalidad(DetailView):
	model = Localidad
	template_name = 'localidad/detalle.html'
	context_object_name = 'localidad'
	
	def get_context_data(self, **kwargs):
		context = super(DetalleLocalidad, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de Localidad'
		context['botones'] = {
			
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

			}
		return context

