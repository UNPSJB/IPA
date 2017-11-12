from django.urls import reverse_lazy, reverse
from ..models import Permiso
from ..forms import PermisoForm
from django.views.generic import ListView,CreateView,DeleteView,DetailView

class AltaSolicitud(CreateView):
	model = Permiso
	form_class = PermisoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('solicitudes:listar')

	def get_context_data(self, **kwargs):
		context = super(AltaSolicitud, self).get_context_data(**kwargs)
		context['nombreForm'] = "Nueva Solicitud"
		context['headers'] = ['Solicitante', 'Establecimiento', 'Tipo', 'Afluente']
		context['botones'] = {
				'Listado': reverse('solicitudes:listar'),
				'Agregar Persona' : reverse('personas:alta'),
			  	'Agregar Establecimiento': reverse('establecimientos:alta'),
			  	'Agregar Tipo de Uso': reverse('tiposDeUso:alta'),
			  	'Agregar Afluente': reverse('afluentes:alta'),
		}
		return context


class DetalleSolicitud(DetailView):
	model = Permiso
	template_name = 'permiso/detalle.html'		

class ListadoSolicitudes(ListView):
	model = Permiso
	template_name = 'solicitudes/listado.html'
	context_object_name = 'solicitudes'

	def get_context_data(self, **kwargs):
		context = super(ListadoSolicitudes, self).get_context_data(**kwargs)
		context['nombreLista'] = "Lista de Solicitudes"
		context['nombreReverse'] = "Solicitudes"
		context['headers'] = ['Solicitante', 'Establecimiento', 'Tipo', 'Estado']
		context['botones'] = {'Alta': reverse('solicitudes:alta')}
		return context

class SolicitudDelete(DeleteView):
	model = Permiso
	template_name = 'permiso/delete.html'
	success_url = reverse_lazy('permisos:listar')
