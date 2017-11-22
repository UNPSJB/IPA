from django.shortcuts import render
from apps.personas.forms import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from apps.personas import models as pmodels
# Create your views here.

from django.views.generic import CreateView, ListView, DetailView, FormView, UpdateView, DeleteView


class CreateBaseView(CreateView):
	message_error = "PERSONA YA EXISTE - REINGRESE DATOS"
	
	def get_context_data(self, **kwargs):
		context = super(CreateBaseView, self).get_context_data(**kwargs)
		context['headers'] = []
		context['nombreForm'] = 'Nueva Persona'
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

class AltaDirector(CreateBaseView):
	model = pmodels.Director
	form_class = DirectorForm
	template_name = 'directores/forms.html'
	success_url = reverse_lazy('directores:listado')
	
	def get_context_data(self, **kwargs):
		context = super(AltaDirector, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Nuevo Director'
		context['message'] = 'Director YA EXISTE'
		return context

	def get(self, request, *args, **kwargs):
		persona = pmodels.Persona.objects.get(pk=kwargs.get('pk'))
		#form = DirectorForm(initial={'persona': persona,'nombre': 'pepe2'})
		form = DirectorForm()
		return render(request, self.template_name, {'form': form, 'persona':persona, 'botones':'', 'rol': self.__class__.model.__name__})
		#return super(PublisherDetail, self).get(request, *args, **kwargs)
		
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		persona = pmodels.Persona.objects.get(pk=kwargs.get('pk'))
		if form.is_valid() and not(persona.sos(Director)):
			director = form.save()
			persona.agregar_rol(director)
			#director.save()
			return HttpResponseRedirect(self.get_success_url())
		return self.render_to_response(self.get_context_data(form=form))

class ListadoDirectores(ListView):
	model = pmodels.Director
	template_name = 'directores/listado.html'
	form_class = DirectorForm

	def get_context_data(self, **kwargs):
		context = super(ListadoDirectores, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Nuevo Director'
		context['botones'] = {'Volver a Listado de Personas': reverse('personas:listado')}
		context['nombreReverse'] = 'directores'
		context['headers'] = ['Nombre y Apellido', 'Legajo','Cargo', 'Fecha de Inicio']
		context['directores'] = pmodels.Director.objects.all()
		return context

class ModificarDirector(UpdateView):
	model = pmodels.Director
	template_name = 'forms.html'
	form_class = DirectorForm
	success_url = reverse_lazy('directores:listado')

	def get_context_data(self, **kwargs):
		context = super(ModificarDirector, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Editar Director:' + self.object.persona.nombre + self.object.persona.apellido
		context['botones'] = {'Volver a Listado de Directores': reverse('directores:listado')}
		return context

class EliminarDirector(DeleteView):
	model = pmodels.Director
	template_name = 'delete.html'
	success_url = reverse_lazy('directores:listado')

	def get_context_data(self, **kwargs):
		context = super(EliminarDirector, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Editar Director:' + self.object.persona.nombre + self.object.persona.apellido
		context['botones'] = {}
		return context