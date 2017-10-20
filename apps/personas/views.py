from django.shortcuts import render
from .forms import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
# Create your views here.

from .models import *

from django.views.generic import CreateView

class AltaPersona(CreateView):
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

class AltaDirector(CreateView):
	model = Director
	form_class = DirectorForm
	template_name = 'forms.html'
	success_url = reverse_lazy('admin:index')
	
	
	def get_context_data(self, **kwargs):
		context = super(AltaDirector, self).get_context_data(**kwargs)
		context['botones'] = {'Alta': '/personas/alta_director', 'Listado':'#'}
		context['nombreForm'] = 'Director'
		return context