from django.shortcuts import render
from apps.personas.forms import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from apps.personas import models as pmodels
# Create your views here.

from ..models import *

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

class AltaAdministrativo(CreateBaseView):
	model = Administrativo
	form_class = AdministrativoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('personas:listado')
	
	def get_context_data(self, **kwargs):
		context = super(AltaAdministrativo, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Nuevo Administrativo'
		context['message'] = 'Administrativo YA EXISTE'
		return context

	def get(self, request, *args, **kwargs):
		persona = pmodels.Persona.objects.get(pk=kwargs.get('pk'))
		#form = DirectorForm(initial={'persona': persona,'nombre': 'pepe2'})
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