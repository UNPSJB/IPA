from django.urls import reverse_lazy, reverse
from ..models import Permiso
from ..forms import PermisoForm
from django.views.generic import ListView,DeleteView,DetailView
from django.shortcuts import redirect
from django.views import View

class ListadoPermisos(ListView):
	model = Permiso
	template_name = 'permisos/listado.html'
	context_object_name = 'permisos'

	def get_context_data(self, **kwargs):
		context = super(ListadoPermisos, self).get_context_data(**kwargs)
		context['nombreLista'] = "Listado de Permisos"
		context['headers'] = ['Solicitante', 'Establecimiento', 'Tipo', 'Afluente', 'Estado', 'Acción', 'Detalle']
		context['botones'] = {
		'Solicitudes': reverse('solicitudes:listar'),
		'Con Expedientes': reverse('permisos:listarPermisosCompletos'),
		'Publicados': reverse('permisos:listarPermisosPublicados'),
		'Otorgados': reverse('permisos:listarPermisosOtorgados'),
		'Bajas': reverse('permisos:listarPermisosDeBaja'),
		'Salir': reverse('index')}
		return context

class PermisoDelete(DeleteView):
	model = Permiso
	template_name = 'delete.html'
	success_url = reverse_lazy('permisos:listar')


class ListadoPermisosDocumentacionCompleta(ListView):
	model = Permiso
	template_name = 'completos/listado.html'
	context_object_name = 'permisos'

	def get_context_data(self, **kwargs):
		context = super(ListadoPermisosDocumentacionCompleta, self).get_context_data(**kwargs)
		context['nombreLista'] = "Lista de Permisos con Documentación Completa"
		context['headers'] = ['Solicitante', 'Establecimiento', 'Tipo', 'Estado']
		context['botones'] = {
		'Alta': reverse('solicitudes:alta'),
		'Volver a Listado de Permisos': reverse('permisos:listar')}
		return context

class DetallePermisoCompleto(DetailView):
	model = Permiso
	template_name = 'completos/detalle.html'
	context_object_name = 'permiso'		

	def get_context_data(self, *args, **kwargs):
		context = super(DetallePermisoCompleto, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de Permiso Completo'
		context['botones'] = {
			'Listado': reverse('solicitudes:listar'),
			'Ver Documentación Presentada': reverse('solicitudes:listarDocumentacionPresentada', args=[self.object.pk]),
			#'Cargar documento': reverse('documentos:alta', pk=kwargs.get.('pk'),
			'Eliminar Solicitud': reverse('solicitudes:eliminar', args=[self.object.pk]),
		}
		return context


class ListadoPermisosPublicados(ListView):
	model = Permiso
	template_name = 'publicados/listado.html'
	context_object_name = 'permisos'

	def get_context_data(self, **kwargs):
		context = super(ListadoPermisosPublicados, self).get_context_data(**kwargs)
		context['nombreLista'] = "Lista de Permisos Publicados"
		context['headers'] = ['Solicitante', 'Establecimiento', 'Tipo', 'Estado']
		context['botones'] = {
		'Alta': reverse('solicitudes:alta'),
		'Volver a Listado de Permisos': reverse('permisos:listar')}
		return context

class DetallePermisoPublicado(DetailView):
	model = Permiso
	template_name = 'publicados/detalle.html'
	context_object_name = 'permiso'		

	def get_context_data(self, *args, **kwargs):
		context = super(DetallePermisoPublicado, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de Permiso Publicado'
		context['botones'] = {
			'Listado': reverse('solicitudes:listar'),
			'Ver Documentación Presentada': reverse('solicitudes:listarDocumentacionPresentada', args=[self.object.pk]),
			#'Cargar documento': reverse('documentos:alta', pk=kwargs.get.('pk'),
			'Eliminar Solicitud': reverse('solicitudes:eliminar', args=[self.object.pk]),
		}
		return context

class ListadoPermisosOtorgados(ListView):
	model = Permiso
	template_name = 'otorgados/listado.html'
	context_object_name = 'permisos'

	def get_context_data(self, **kwargs):
		context = super(ListadoPermisosOtorgados, self).get_context_data(**kwargs)
		context['nombreLista'] = "Lista de Permisos Otorgados"
		context['headers'] = ['Solicitante', 'Establecimiento', 'Tipo', 'Estado']
		context['botones'] = {
		'Alta': reverse('solicitudes:alta'),
		'Volver a Listado de Permisos': reverse('permisos:listar')}
		return context

class DetallePermisoOtorgado(DetailView):
	model = Permiso
	template_name = 'otorgados/detalle.html'
	context_object_name = 'permiso'		

	def get_context_data(self, *args, **kwargs):
		context = super(DetallePermisoOtorgado, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de Permiso Otorgado'
		context['botones'] = {
			'Calcular Canon': reverse('pagos:altaCobro', args=[self.permiso_pk]),
			'Ver Listado de Cobros': reverse('pagos:listarCobros', args=[self.permiso_pk]),
			'Listado': reverse('solicitudes:listar'),
			'Ver Documentación Presentada': reverse('solicitudes:listarDocumentacionPresentada', args=[self.object.pk]),
			'Eliminar Solicitud': reverse('solicitudes:eliminar', args=[self.object.pk]),
		}
		return context

	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		return super(DetallePermisoOtorgado, self).get(request,*args,**kwargs)

class ListadoPermisosDeBaja(ListView):
	model = Permiso
	template_name = 'bajas/listado.html'
	context_object_name = 'permisos'

	def get_context_data(self, **kwargs):
		context = super(ListadoPermisosDeBaja, self).get_context_data(**kwargs)
		context['nombreLista'] = "Lista de Permisos dados de Baja"
		context['headers'] = ['Solicitante', 'Establecimiento', 'Tipo', 'Estado']
		context['botones'] = {
		'Alta': reverse('solicitudes:alta'),
		'Volver a Listado de Permisos': reverse('permisos:listar')}
		return context

class DetallePermisoDeBaja(DetailView):
	model = Permiso
	template_name = 'bajas/detalle.html'
	context_object_name = 'permiso'		

	def get_context_data(self, *args, **kwargs):
		context = super(DetallePermisoDeBaja, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de Permiso dado de Baja'
		context['botones'] = {
			'Volver a Lista de Permisos dados de Baja': reverse('permisos:listarPermisosDeBaja'),
			'Ver Documentación Presentada': reverse('solicitudes:listarDocumentacionPresentada', args=[self.object.pk]),
			'Eliminar Solicitud': reverse('solicitudes:eliminar', args=[self.object.pk]),
		}
		return context

class DetallePermiso(View):
	def get(self, request,*args, **kwargs):
		id_permiso = kwargs['pk']
		permiso = Permiso.objects.get(pk=id_permiso)
		if permiso.estado().tipo == 1 or permiso.estado().tipo == 2:
			url = reverse('solicitudes:detalle', args=[id_permiso] )
		elif permiso.estado().tipo == 3:
			url = reverse('permisos:detallePermisoCompleto', args=[id_permiso])
		elif permiso.estado().tipo == 4:
			return redirect(reverse('permisos:detallePermisoPublicado', args=[id_permiso]))
		elif permiso.estado().tipo == 5:
			url = reverse('permisos:detallePermisoOtorgado', args=[id_permiso])
		elif permiso.estado().tipo == 6:
			url = reverse('permisos:detallePermisoDeBaja', args=[id_permiso])
		else:
			url = reverse('permisos:listar')
		return redirect(url)