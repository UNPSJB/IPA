from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Expediente
from django.views.generic import ListView,CreateView,DeleteView,DetailView


# Create your views here.

class AltaExpediente(CreateView):
	model = Expediente
	form_class = ExpedienteForm
	template_name = 'forms.html' 
	success_url = reverse_lazy('expediente:listadoExpediente')

	def get_context_data(self, **kwargs):
		context = super(AltaExpediente, self).get_context_data(**kwargs)
		context['nombreLista'] = "Expediente"
		context['headers'] = ['Fecha', 'Numero', 'Extracto']
		context['botones'] = {'Alta': '/expediente/alta', 'Listado':'/expediente/listar'}
		return context
	

class DetalleExpediente(DetailView):
	model = Expediente
	template_name = 'expediente/detalle.html'		

class ListadoExpediente(ListView):
	model = Expediente
	template_name = 'expediente/listado.html'
	context_object_name = 'expedientes'

	def get_context_data(self, **kwargs):
		context = super(ListadoExpediente, self).get_context_data(**kwargs)
		context['nombreLista'] = "Expediente"
		context['headers'] = ['Fecha', 'Solicitante', 'Tipo']
		context['botones'] = {'Alta': '/expediente/alta', 'Listado':'/expediente/listar'}
		return context

class DeleteExpediente(DeleteView):
	model = Expediente
	template_name = 'expediente/delete.html'
	success_url = reverse_lazy('permisos:listadoExpediente')
