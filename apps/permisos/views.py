from django.urls import reverse_lazy
from .models import Solicitud, Permiso
from .forms import SolicitudForm, PermisoForm
from django.views.generic import ListView,CreateView,DeleteView,DetailView


# Create your views here.

#Solicitudes
class AltaSolicitud(CreateView):
	model = Solicitud
	form_class = SolicitudForm
	template_name = 'solicitud/alta.html'
	success_url = reverse_lazy('permisos:listadoSolicitud')

class DetalleSolicitud(DetailView):
	model = Solicitud
	template_name = 'solicitud/detalle.html'		

class ListadoSolicitudes(ListView):
	model = Solicitud
	template_name = 'solicitud/listado.html'
	context_object_name = 'solicitudes'

	def get_context_data(self, **kwargs):
		context = super(ListadoSolicitudes, self).get_context_data(**kwargs)
		context['nombreLista'] = "Solicitudes"
		context['headers'] = ['Fecha', 'Solicitante', 'Tipo']
		context['botones'] = {'Alta': '/permisos/solicitudes/alta', 'Listado':'/permisos/documentos/listar'}
		return context

class SolicitudDelete(DeleteView):
	model = Solicitud
	template_name = 'solicitud/delete.html'
	success_url = reverse_lazy('permisos:listadoSolicitud')

#Permisos
class AltaPermiso(CreateView):
	model = Permiso
	form_class = PermisoForm
	template_name = 'permiso/alta.html'
	success_url = reverse_lazy('permisos:listadoPermiso')

class DetallePermiso(DetailView):
	model = Permiso
	template_name = 'permiso/detalle.html'		

class ListadoPermisos(ListView):
	model = Permiso
	template_name = 'permiso/listado.html'
	context_object_name = 'permisos'

	def get_context_data(self, **kwargs):
		context = super(ListadoPermisos, self).get_context_data(**kwargs)
		context['nombreLista'] = "Permisos"
		context['headers'] = ['Fecha', 'Solicitante', 'Tipo']
		context['botones'] = {'Alta': '/permisos/alta', 'Listado':'/permisos/listar'}
		return context

class PermisoDelete(DeleteView):
	model = Permiso
	template_name = 'permiso/delete.html'
	success_url = reverse_lazy('permisos:listadoPermiso')
