from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from apps.personas import models as pmodels
# Create your views here.

from apps.personas.forms import *
from django.views.generic import CreateView, ListView, DetailView, FormView, UpdateView, DeleteView


class CreateBaseView(CreateView):
	message_error = "PERSONA YA EXISTE - REINGRESE DATOS"
	
	def get_context_data(self, **kwargs):
		context = super(CreateBaseView, self).get_context_data(**kwargs)
		context['headers'] = []
		context['nombreForm'] = 'Nueva persona'
		context['botones'] = {
			'Nueva Persona': reverse('personas:alta'), 
			'Directores':'', 
			'Administrativos':'', 
			'Liquidadores':''
		}
		return context

	def form_valid(self,form):
		self.object = form.save()
		if self.object != None:
			return HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form, message = "PERSONA YA EXISTE - REINGRESE DATOS"))

class AltaPersona(CreateBaseView):
	model = pmodels.Persona
	form_class = PersonaForm
	template_name = 'forms.html'
	success_url = reverse_lazy('personas:listado')

	def get_context_data(self, **kwargs):
		context = super(AltaPersona, self).get_context_data(**kwargs)
		context['botones'] = {
			'Volver a listado de Personas':reverse('personas:listado')
		}
		return context

class ModificarPersona(UpdateView):
	model = pmodels.Persona
	template_name = 'forms.html'
	form_class = PersonaForm
	success_url = reverse_lazy('personas:listado')

	def get_context_data(self, **kwargs):
		context = super(ModificarPersona, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Editar Persona:'
		context['botones'] = {'Volver a listado de Personas':reverse('personas:listado')}
		return context

class ListadoPersonas(ListView):
	model = pmodels.Persona
	template_name = 'personas/listado.html'
	context_object_name = 'personas'

	def get_context_data(self, **kwargs):
		context = super(ListadoPersonas, self).get_context_data(**kwargs)
		context['botones'] = {
			'Alta Persona': reverse('personas:alta'),
		 	'Directores':reverse('directores:listado'), 
		 	'Administrativos':'', 
		 	'Liquidadores':''
		 }
		context['nombreReverse'] = 'personas'
		context['headers'] = ['Nombre', 'Apellido','Tipo de Documento', 'Numero de Documento']
		return context

class DetallePersona(DetailView):
	model = pmodels.Persona
	form_class = DetallePersonaForm
	template_name = 'personas/detalle.html'
	context_object_name = 'persona'

	def get_context_data(self, **kwargs):
		context = super(DetallePersona, self).get_context_data(**kwargs)
		context['botones'] = {
			'Volver a las Personas': reverse('personas:listado'),
			'Nueva Persona': reverse('personas:alta'), 
			'Directores': reverse('directores:listado'), 
			'Administrativos':'', 
			'Liquidadores':''
		}
		context['roles'] = pmodels.Rol.TIPOS 
		return context