from django.urls import reverse_lazy, reverse
from ..models import Permiso
from ..forms import PermisoForm
from django.views.generic import ListView,CreateView,DeleteView,DetailView

class AltaSolicitud(CreateView):
	model = Permiso
	form_class = PermisoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('permisos:listar')

	def get_context_data(self, **kwargs):
		context = super(AltaPermiso, self).get_context_data(**kwargs)
		context['nombreLista'] = "Permisos"
		context['headers'] = ['Solicitante', 'Establecimiento', 'Tipo', 'Afluente']
		context['botones'] = {'Alta': reverse('solicitudes:alta'), 'Listado': reverse('solicitudes:listar')}
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
