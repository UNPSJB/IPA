from django.urls import reverse_lazy, reverse
from ..models import TipoUso
from ..forms import TipoDeUsoForm
from django.views.generic import ListView,CreateView,DeleteView,DetailView

# Create your views here.
class AltaTipoDeUso(CreateView):
	model = TipoUso
	form_class = TipoDeUsoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('tiposDeUso:listar')
	


	def get_context_data(self, **kwargs):
		context = super(AltaTipoDeUso, self).get_context_data(**kwargs)
		context['botones'] = {
			'Alta': reverse('tiposDeUso:alta')
			}
		context['nombreForm'] = 'Nuevo tipo de uso'
		return context

class DetalleTipoDeUso(DetailView):
	model = TipoUso
	template_name = 'tipoDeUso/detalle.html'		
	context_object_name = 'tipo'
	
	def get_context_data(self, **kwargs):
		context = super(DetalleTipoDeUso, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de tipo de uso'
		context['botones'] = {
			'Listado': reverse('tiposDeUso:listar'),
			'Nuevo tipo de uso': reverse('tiposDeUso:alta'),
			'Eliminar tipo de uso': reverse('tiposDeUso:eliminar', args=[self.object.id])
		}
		return context
class ListadoTiposDeUso(ListView):
	model = TipoUso
	template_name = 'tipoDeUso/listado.html'
	context_object_name = 'tiposDeUso'

	def get_context_data(self, **kwargs):
		context = super(ListadoTiposDeUso, self).get_context_data(**kwargs)
		context['nombreLista'] = "Listado de tipos de uso"
		context['nombreReverse'] = "tiposDeUso"
		context['headers'] = ['Nombre', 'Coeficiente', 'Periodo']
		context['botones'] = {
			'Alta': reverse('tiposDeUso:alta') 
			}
		return context

class DeleteTipoDeUso(DeleteView):
	model = TipoUso
	template_name = 'delete.html'
	success_url = reverse_lazy('tiposDeUso:listar')