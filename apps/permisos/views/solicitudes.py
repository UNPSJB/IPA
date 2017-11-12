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
							  	'Agregar Persona' : reverse('personas:alta_personas'),
							  	'Agregar Establecimiento': reverse('establecimientos:altaEstablecimiento'),
							  	'Agregar Tipo de Uso': reverse('tiposDeUso:alta'),
							  	'Agregar Afluente': reverse('establecimientos:alta_afluente'),
							  }
		return context


class DetalleSolicitud(DetailView):
	model = Permiso
	template_name = 'permiso/detalle.html'		

class ListadoSolicitudes(ListView):
	model = Permiso
	template_name = 'permisos/listado.html'
	context_object_name = 'permisos'

	def get_context_data(self, **kwargs):
		context = super(ListadoSolicitudes, self).get_context_data(**kwargs)
		context['nombreLista'] = "Permisos"
		context['headers'] = ['Solicitante', 'Establecimiento', 'Tipo', 'Afluente']
		context['botones'] = {'Alta': reverse('permisos:alta'), 'Listado': reverse('permisos:listar')}
		return context

class SolicitudDelete(DeleteView):
	model = Permiso
	template_name = 'permiso/delete.html'
	success_url = reverse_lazy('permisos:listar')
