from django.shortcuts import render
from django.urls import reverse_lazy
from .models import TipoDocumentacion
from .forms import AltaForm
from django.views.generic import ListView,CreateView,DeleteView,DetailView


# Create your views here.
class AltaTipoDocumentacion(CreateView):
	model = TipoDocumentacion
	form_class = AltaForm
	template_name = 'tipoDocumentacion/alta.html'
	success_url = reverse_lazy('tipoDocumentacion:listado')

class DetalleTipoDocumentacion(DetailView):
	model = TipoDocumentacion
	template_name = 'tipoDocumentacion/detalle.html'		

class ListadoTipoDocumentacion(ListView):
	model = TipoDocumentacion
	#form_class = AfluenteForm
	template_name = 'tipoDocumentacion/listado.html'
	context_object_name = 'documentos'

	def get_context_data(self, **kwargs):
		context = super(ListadoTipoDocumentacion, self).get_context_data(**kwargs)
		context['nombreLista'] = "Tipos de Documentación"
		context['headers'] = ['Nombre']
		context['botones'] = {'Alta': '/documentos/alta', 'Listado':'/documentos/listar'}
		return context


class TipoDocumentacionDelete(DeleteView):
	model = TipoDocumentacion
	template_name = 'tipoDocumentacion/delete.html'
	success_url = reverse_lazy('tipoDocumentacion:listado')
