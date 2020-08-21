from django.urls import reverse_lazy, reverse
from ..models import Permiso
from ..forms import PermisoForm, SolicitadoForm
from django.views import View
from django.shortcuts import render, redirect
from django.views.generic import ListView,DeleteView,DetailView

from datetime import datetime

class DetalleSolicitud(DetailView):
	model = Permiso
	template_name = 'permisos/detalle.html'
	context_object_name = 'solicitud'		

	def get_context_data(self, *args, **kwargs):
		context = super(DetalleSolicitud, self).get_context_data(**kwargs)
		print(self.object)
		context['nombreDetalle'] = 'Detalle de la Solicitud'
		context['botones'] = {
			'Listado': reverse('solicitudes:listar'),
			'Ver Documentación Presentada': reverse('solicitudes:listarDocumentacionPresentada', args=[self.object.pk]),
			'Nueva acta de Inspeccion': reverse('actas:altaInspeccion',  args=[self.object.pk]),
			'Nueva acta de Infraccion': reverse('actas:altaInfraccion',  args=[self.object.pk]),
			'Eliminar Solicitud': reverse('solicitudes:eliminar', args=[self.object.pk]),
			#'Agregar Infracción': reverse('documentos:agregarInfraccion', args=[self.object.pk]),
		}
		return context

class ListadoDocumentacionPresentada(DetailView):
	model = Permiso
	template_name = 'permisos/listadoDocumentacionPresentada.html'
	context_object_name = 'permiso'

	def get_context_data(self, **kwargs):
		context = super(ListadoDocumentacionPresentada, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de Documentos'
		context['headers'] = ['Tipo', 'Descripción', 'Fecha']
		context['botones'] = {
			'Volver a Detalle de la Solicitud': reverse('permisos:detalle', args=[self.object.pk])}
		return context

class ListadoSolicitudes(ListView):
	model = Permiso
	template_name = 'solicitudes/listado.html'
	context_object_name = 'solicitudes'

	def get_context_data(self, **kwargs):
		context = super(ListadoSolicitudes, self).get_context_data(**kwargs)
		context['nombreLista'] = "Lista de Solicitudes"
		context['nombreReverse'] = "solicitudes"
		context['headers'] = ['Solicitante', 'Establecimiento', 'Tipo de Uso de Agua', 'Estado', 'Acción', 'Detalle']
		context['botones'] = {

		'Nuevo': reverse('solicitudes:alta'),
		'Volver a Listado de Permisos': reverse('permisos:listar')}
		return context


class SolicitudDelete(DeleteView):
	model = Permiso
	template_name = 'delete.html'
	success_url = reverse_lazy('permisos:listar')



def visar_documento_solicitud(request,pks,pkd):
	permiso = Permiso.objects.get(pk=pks)
	documento = permiso.documentos.get(pk=pkd)
	permiso.hacer('revisar',request.user, datetime.now(), [documento])
	return redirect('solicitudes:listarDocumentacionPresentada', pks)

