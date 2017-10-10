from django.urls import reverse_lazy
from .models import TipoUso
from .forms import AltaForm
from django.views.generic import ListView,CreateView,DeleteView,DetailView


# Create your views here.
class AltaTipoDeUso(CreateView):
	model = TipoUso
	form_class = AltaForm
	template_name = 'tipoDeUso/alta.html'
	success_url = reverse_lazy('tiposDeUso:listado')

class DetalleTipoDeUso(DetailView):
	model = TipoUso
	template_name = 'tipoDeUso/detalle.html'		

class ListadoTiposDeUso(ListView):
	model = TipoUso
	template_name = 'tipoDeUso/listado.html'
	context_object_name = 'tiposDeUso'

	def get_context_data(self, **kwargs):
		context = super(ListadoTiposDeUso, self).get_context_data(**kwargs)
		context['nombreLista'] = "Tipos de Uso"
		context['headers'] = ['Nombre', 'Coeficiente', 'Periodo']
		context['botones'] = {'Alta': '/documentos/alta', 'Listado':'/documentos/listar'}
		return context

class TipoDeUsoDelete(DeleteView):
	model = TipoUso
	template_name = 'tipoDeUso/delete.html'
	success_url = reverse_lazy('tiposDeUso:listado')
