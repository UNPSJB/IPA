from django.shortcuts import render
from .forms import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
# Create your views here.

from .models import *

from django.views.generic import CreateView

class BaseView(CreateView):
	def form_valid(self,form):
		self.object = form.save()
		if self.object != None:
			return HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form, message = self.message_error))

class AltaPersona(BaseView):
	model = Persona
	form_class = PersonaForm
	template_name = 'forms.html'
	#success_url = reverse_lazy('afluentes:listar_afluentes')
	#
	#
	def get_context_data(self, **kwargs):
		context = super(AltaPersona, self).get_context_data(**kwargs)
		context['botones'] = {'Alta': '/personas/alta_personas', 'Listado':'#'}
		context['nombreForm'] = 'Personas'
		return context

class AltaDirector(BaseView):
	model = Director
	form_class = DirectorForm
	template_name = 'forms.html'
	success_url = reverse_lazy('admin:index')
	message_error = "DIRECTO YA EXISTE - REINGRESE DATOS"
	
	def get_context_data(self, **kwargs):
		context = super(AltaDirector, self).get_context_data(**kwargs)
		context['botones'] = {'Alta': '/personas/alta_director', 'Listado':'#'}
		context['nombreForm'] = 'Director'
		return context

class AltaAdministrativo(BaseView):
	model = Administrativo
	form_class = AdministrativoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('admin:index')
	message_error = "Administrativo YA EXISTE - REINGRESE DATOS"
	
	def get_context_data(self, **kwargs):
		context = super(AltaAdministrativo, self).get_context_data(**kwargs)
		context['botones'] = {'Alta': '#', 'Listado':'#'}
		context['nombreForm'] = 'Administrativo'
		return context