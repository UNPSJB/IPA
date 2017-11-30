from django.shortcuts import render
from apps.personas.forms import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from apps.personas import models as pmodels
# Create your views here.

from django.views.generic import CreateView, ListView, UpdateView, DeleteView


class AltaChofer(CreateView):
	model = pmodels.Chofer
	form_class = ChoferForm
	template_name = 'forms.html'
	success_url = reverse_lazy('personas:listado')
	
	def get_context_data(self, **kwargs):
		context = super(AltaDirector, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Nuevo Chofer'
		context['message'] = 'Chofer YA EXISTE'
		return context

	def get(self, request, *args, **kwargs):
		persona = pmodels.Persona.objects.get(pk=kwargs.get('pk'))
		form = ChoferForm()
		return render(request, self.template_name, {'form': form, 'persona':persona, 'botones':'', 'rol': self.__class__.model.__name__})
		
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		persona = pmodels.Persona.objects.get(pk=kwargs.get('pk'))
		if form.is_valid() and not(persona.sos(Chofer)):
			chofer = form.save()
			persona.agregar_rol(chofer)
			return HttpResponseRedirect(self.get_success_url())
		return self.render_to_response(self.get_context_data(form=form))

class ListadoChoferes(ListView):
	model = pmodels.Chofer
	template_name = 'choferes/listado.html'

	def get_context_data(self, **kwargs):
		context = super(ListadoChoferes, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Listado de Choferes'
		context['botones'] = {'Volver a Listado de Personas': reverse('personas:listado')}
		context['nombreReverse'] = 'choferes'
		context['headers'] = ['Nombre y Apellido', 'Licencia', 'Fecha de Vencimiento de Licencia']
		context['choferes'] = pmodels.Chofer.objects.all()
		return context

class ModificarChofer(UpdateView):
	model = pmodels.Chofer
	template_name = 'forms.html'
	form_class = ChoferForm
	success_url = reverse_lazy('choferes:listado')

	def get_context_data(self, **kwargs):
		context = super(ModificarChofer, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Editar Chofer: ' + self.object.persona.nombre + self.object.persona.apellido
		context['botones'] = {'Volver a Listado de Choferes': reverse('choferes:listado')}
		return context

class EliminarChofer(DeleteView):
	model = pmodels.Chofer
	template_name = 'delete.html'
	success_url = reverse_lazy('choferes:listado')

	def get_context_data(self, **kwargs):
		context = super(EliminarChofer, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Eliminar Chofer:'
		context['botones'] = {}
		return context