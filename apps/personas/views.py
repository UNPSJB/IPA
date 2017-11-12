from django.shortcuts import render
from .forms import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from apps.personas import models as pmodels
# Create your views here.

from .models import *

from django.views.generic import CreateView, ListView, DetailView, FormView


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
	model = Persona
	form_class = PersonaForm
	template_name = 'forms.html'

	def get_context_data(self, **kwargs):
		context = super(AltaPersona, self).get_context_data(**kwargs)
		context['botones'] = {
			'Listado':reverse('personas:listado')
		}
		return context

class ListadoPersonas(ListView):
	model = Persona
	template_name = 'personas/listado.html'
	context_object_name = 'personas'

	def get_context_data(self, **kwargs):
		context = super(ListadoPersonas, self).get_context_data(**kwargs)
		context['botones'] = {
			'Alta Persona': reverse('personas:alta'),
		 	'Directores':'', 
		 	'Administrativos':'', 
		 	'Liquidadores':''
		 }
		context['headers'] = ['Nombre', 'Apellido','Tipo de Documento', 'Numero de Documento']
		return context

class DetallePersona(DetailView):
	model = Persona
	form_class = DetallePersonaForm
	template_name = 'personas/detalle.html'
	context_object_name = 'persona'

	def get_context_data(self, **kwargs):
		context = super(DetallePersona, self).get_context_data(**kwargs)
		context['botones'] = {
			'Nueva Persona': reverse('personas:alta'), 
			'Directores':'', 
			'Administrativos':'', 
			'Liquidadores':''
		}
		context['roles'] = pmodels.Rol.TIPOS 
		return context

class AltaDirector(CreateBaseView):
	model = Director
	form_class = DirectorForm
	template_name = 'personas/forms.html'
	success_url = reverse_lazy('personas:listado')
	
	def get_context_data(self, **kwargs):
		context = super(AltaDirector, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Nuevo director'
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

class AltaAdministrativo(CreateBaseView):
	model = Administrativo
	form_class = AdministrativoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('personas:listado')
	
	def get_context_data(self, **kwargs):
		context = super(AltaAdministrativo, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Nuevo administrativo'
		context['message'] = 'Administrativo YA EXISTE'
		return context

	def get(self, request, *args, **kwargs):
		persona = pmodels.Persona.objects.get(pk=kwargs.get('pk'))
		form = AdministrativoForm()
		return render(request, self.template_name, {'form': form, 'persona':persona, 'botones':'', 'rol': self.__class__.model.__name__})
		
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		persona = pmodels.Persona.objects.get(pk=kwargs.get('pk'))
		if form.is_valid() and not(persona.sos(Administrativo)):
			administrativo = form.save()
			persona.agregar_rol(administrativo)
			#director.save()
			return HttpResponseRedirect(self.get_success_url())
		return self.render_to_response(self.get_context_data(form=form))
