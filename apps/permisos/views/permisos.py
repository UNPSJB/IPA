from django.urls import reverse_lazy, reverse
from ..models import Permiso
from ..forms import PermisoForm, SolicitadoForm
from django.views.generic import ListView,DeleteView,DetailView
from django.shortcuts import redirect
from django.views import View
from datetime import date, datetime
from apps.documentos.views import AltaDocumento
from apps.generales.views import GenericListadoView, GenericAltaView
from ..tables import PermisosTable
from ..filters import PermisosFilter

class ListadoPermisos(GenericListadoView):
	model = Permiso
	template_name = 'permisos/listado.html'
	table_class = PermisosTable
	paginate_by = 12
	filterset_class = PermisosFilter
	

class AltaPermiso(GenericAltaView):
	model = Permiso
	form_class = PermisoForm
	template_name = 'permisos/alta.html'
	success_url = reverse_lazy('permisos:listar')
	message_error = "Permiso existente"
	cargar_otro_url = reverse_lazy('permiso:alta')

	def get_context_data(self, **kwargs):
		context = super(AltaPermiso, self).get_context_data(**kwargs)
		context['solicitadoForm'] = SolicitadoForm()
		return context

	def post(self, request):
		permiso_form = PermisoForm(request.POST)
		solicitado_form = SolicitadoForm(request.POST)
		if permiso_form.is_valid() and solicitado_form.is_valid():
			permiso = permiso_form.save(commit=False)
			permiso.fechaSolicitud = datetime.strptime(solicitado_form.data['fecha'], "%Y-%m-%d").date()
			permiso = permiso_form.save()
			solicitado = solicitado_form.save(commit=False)
			solicitado.permiso = permiso
			solicitado.usuario = request.user
			solicitado.save()
			return redirect('permisos:listar')
		return redirect('permisos:alta')


class PermisoDelete(DeleteView):
	model = Permiso
	template_name = 'delete.html'
	success_url = reverse_lazy('permisos:listar') 

class DetallePermisoPublicado(DetailView):
	model = Permiso
	template_name = 'publicados/detalle.html'
	context_object_name = 'permiso'		

	def get_context_data(self, *args, **kwargs):
		context = super(DetallePermisoPublicado, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de Permiso Publicado'
		context['botones'] = {
			'Nueva acta de Inspeccion': reverse('actas:altaInspeccion',  args=[self.object.pk]),
			'Nueva acta de Infraccion': reverse('actas:altaInfraccion',  args=[self.object.pk]),
			'Listado Permisos Publicados': reverse('permisos:listarPermisosPublicados'),
			'Documentación Presentada': reverse('solicitudes:listarDocumentacionPresentada', args=[self.object.pk]),
			'Eliminar Solicitud': reverse('solicitudes:eliminar', args=[self.object.pk]),
		}
		return context

class DetallePermisoOtorgado(DetailView):
	model = Permiso
	template_name = 'otorgados/detalle.html'
	context_object_name = 'permiso'		

	def get_context_data(self, *args, **kwargs):
		context = super(DetallePermisoOtorgado, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de Permiso Otorgado'
		context['botones'] = {
			'Nueva acta de Inspeccion': reverse('actas:altaInspeccion',  args=[self.object.pk]),
			'Nueva acta de Infraccion': reverse('actas:altaInfraccion',  args=[self.object.pk]),
			'Nuevo Cobro de Infraccion': reverse('pagos:altaCobroInfraccion', args=[self.permiso_pk,]),
			'Nuevo Cobro de Canon': reverse('pagos:altaCobro', args=[self.permiso_pk]),
			'Listado de Cobros': reverse('pagos:listarCobros', args=[self.permiso_pk]),
			'Nuevo Pago de Infraccion': reverse('pagos:AltaPagoInfraccion', args=[self.permiso_pk]),
			'Nuevo Pago de Canon': reverse('pagos:altaPago', args=[self.permiso_pk]),
			'Listado de Pagos': reverse('pagos:listarPagos', args=[self.permiso_pk]),
			'Listado Permisos Otorgados': reverse('permisos:listarPermisosOtorgados'),
			'Documentación Presentada': reverse('solicitudes:listarDocumentacionPresentada', args=[self.object.pk]),
			'Eliminar Solicitud': reverse('solicitudes:eliminar', args=[self.object.pk]),
		}
		return context


	def get (self, request, *args, **kwargs):
		self.permiso_pk = kwargs.get('pk')
		return super(DetallePermisoOtorgado, self).get(request,*args,**kwargs)

class DetallePermisoDeBaja(DetailView):
	model = Permiso
	template_name = 'bajas/detalle.html'
	context_object_name = 'permiso'		

	def get_context_data(self, *args, **kwargs):
		context = super(DetallePermisoDeBaja, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de Permiso dado de Baja'
		context['botones'] = {
			'Nueva acta de Inspeccion': reverse('actas:altaInspeccion',  args=[self.object.pk]),
			'Nueva acta de Infraccion': reverse('actas:altaInfraccion',  args=[self.object.pk]),
			'Volver a Lista de Permisos dados de Baja': reverse('permisos:listarPermisosDeBaja'),
			'Documentación Presentada': reverse('solicitudes:listarDocumentacionPresentada', args=[self.object.pk]),
			'Eliminar Solicitud': reverse('solicitudes:eliminar', args=[self.object.pk]),
		}
		return context

class DetallePermiso(DetailView):
	model = Permiso
	template_name = 'permisos/detalle.html'
	context_object_name = 'solicitud'

	def get_context_data(self, *args, **kwargs):
			context = super(DetallePermiso, self).get_context_data(**kwargs)
			context['botones'] = {
				'Ver Documentación Presentada': reverse('permisos:listarDocumentacionPresentada', args=[self.object.pk]),
				'Nueva acta de Inspeccion': reverse('actas:altaInspeccion',  args=[self.object.pk]),
				'Nueva acta de Infraccion': reverse('actas:altaInfraccion',  args=[self.object.pk]),
				'Eliminar Solicitud': reverse('solicitudes:eliminar', args=[self.object.pk]),
			}
			return context

class ListadoDocumentacionPresentada(DetailView):
	model = Permiso
	template_name = 'permisos/listadoDocumentacionPresentada.html'
	context_object_name = 'permiso'

	def get_context_data(self, **kwargs):
		context = super(ListadoDocumentacionPresentada, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de Documentos'
		context['botones'] = {
			'Volver a Detalle de la Solicitud': reverse('permisos:detalle', args=[self.object.pk])}
		return context

def visar_documento_solicitud(request,pks,pkd):
	permiso = Permiso.objects.get(pk=pks)
	documento = permiso.documentos.get(pk=pkd)
	permiso.hacer('revisar',request.user, datetime.now(), [documento])
	return redirect('permisos:listarDocumentacionPresentada', pks)

class NuevaDocumentacionRequerida(AltaDocumento):
	def get_form(self, form_class):
		form  = self_form_class()
		permiso = Permiso.objects.get(id= self.permiso.pk)
		
		return form 
