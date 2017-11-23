from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from .models import ValorDeModulo, Cobro
from .forms import RegistrarValorDeModuloForm, CobroForm
from django.views.generic import ListView,CreateView,DeleteView


class AltaValorDeModulo(CreateView):
	model = ValorDeModulo
	form_class = RegistrarValorDeModuloForm
	template_name = 'forms.html'
	success_url = reverse_lazy('pagos:listarModulos')

	def get_context_data(self, **kwargs):
		context = super(AltaValorDeModulo, self).get_context_data(**kwargs)
		context['nombreForm'] = "Alta Valor de Modulo"
		context['headers'] = ['']
		context['botones'] = {
			'Listado':reverse('tipoDocumentos:listar'),
			}
		return context

class ListadoValoresDeModulo(ListView):
	model = ValorDeModulo
	template_name = 'modulos/listado.html'
	context_object_name = 'modulos'

	def get_context_data(self, **kwargs):
		context = super(ListadoValoresDeModulo, self).get_context_data(**kwargs)
		context['nombreLista'] = "Listado de tipos de documento"
		context['headers'] = ['Precio', 'Fecha', 'Descripcion', 'Detalle']
		context['botones'] = {
			'Alta Valor de Modulo': reverse('pagos:altaModulo'),
			'Salir': reverse('index')
			}
		return context

class EliminarValorDeModulo(DeleteView):
	model = ValorDeModulo
	template_name = 'delete.html'
	success_url = reverse_lazy('pagos:listarModulos')

class AltaCobro(CreateView):
	model = Cobro
	form_class = CobroForm
	template_name = 'forms.html'
	success_url = reverse_lazy('pagos:listarModulos')

	def get_context_data(self, **kwargs):
		context = super(AltaCobro, self).get_context_data(**kwargs)
		context['nombreForm'] = "Alta Valor de Modulo"
		context['headers'] = ['']
		context['botones'] = {
			'Listado':reverse('tipoDocumentos:listar'),
			}
		return context