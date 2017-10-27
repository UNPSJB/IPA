from .forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .models import Oposicion
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView

class AltaOposicion(CreateView):
	model = Oposicion
	form_class = OposicionForm
	template_name = 'forms.html'
	success_url = reverse_lazy('oposicion:listado')

	def get_context_data(self, **kwargs):
		context = super(AltaOposicion, self).get_context_data(**kwargs)
		context['botones'] = {
		  'Alta': reverse('oposicion:alta'), 
		  'Listado': reverse('oposicion:listado')
		}
		context['nombreForm'] = 'Oposicion'
		return context

class DetalleOposicion(DetailView):
	model = Oposicion
	template_name = 'oposicion/detalleOposicion.html'		


class ListadoOpisicion(ListView):
	model = Oposicion
	template_name = 'oposicion/listado.html'
	context_object_name = 'oposiciones'


	def get_context_data(self, **kwargs):
		context = super(ListadoOpisicion, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Oposiciones'
		context['headers'] = ['Numero', 'Fecha','Persona']
		context['botones'] = {'Alta': '/oposicion/alta', 'Listado':'/oposicion/listado'}
		return context

class ModificarOposicion(UpdateView):
	model = Oposicion
	form_class = OposicionForm
	template_name = 'oposicion/form.html'
	success_url = reverse_lazy('oposicion:listado')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_oposicion = kwargs['pk']
		oposicion = self.model.objects.get(id=id_oposicion)
		form = self.form_class(request.POST, instance=oposicion)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())


class OposicionDelete(DeleteView):
	model = Oposicion
	template_name = 'Oposicion/delete.html'
	success_url = reverse_lazy('oposicion:listado')