from django.urls import reverse_lazy, reverse
from ..models import Solicitado, Publicado, Permiso, Otorgado, Baja, Archivado
from ..forms import PermisoForm, SolicitadoForm
from django.views.generic import ListView,DeleteView,DetailView,UpdateView
from django.shortcuts import redirect
from django.views import View
from datetime import date, datetime
from apps.documentos.views import AltaDocumento
from apps.generales.views import GenericListadoView, GenericAltaView,GenericEliminarView
from ..tables import PermisosTable
from ..filters import PermisosFilter


class ListadoPermisos(GenericListadoView):
	model = Permiso
	template_name = 'permisos/listado.html'
	table_class = PermisosTable
	paginate_by = 12
	filterset_class = PermisosFilter
	context_object_name = 'permiso'
	export_name = 'listado_permisos'
	

class AltaPermiso(GenericAltaView):
	model = Permiso
	form_class = PermisoForm
	template_name = 'permisos/alta.html'
	success_url = reverse_lazy('permisos:listar')
	message_error = ["Permiso existente"]
	cargar_otro_url = reverse_lazy('permiso:alta')

	def get_context_data(self, **kwargs):
		context = super(AltaPermiso, self).get_context_data(**kwargs)
		context['solicitadoForm'] = SolicitadoForm()
		context['ayuda'] = 'solicitud.html#como-crear-un-nuevo-permiso'
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

class ModificarPermiso(UpdateView):
	model = Permiso
	form_class = PermisoForm
	template_name = 'permisos/alta.html'
	success_url = reverse_lazy('permisos:listar')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_permiso = kwargs['pk']
		permiso = self.model.objects.get(pk=pks)
		form = self.form_class(request.POST, instance=permiso)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		context = super(ModificarPermiso, self).get_context_data(**kwargs)
		context['nombreForm'] = "Modificar Permiso"
		context['return_path'] = reverse('permisos:listar')
		return context


#class PermisoDelete(DeleteView):
class PermisoDelete(GenericEliminarView):
	model = Permiso
	template_name = 'delete.html'
	success_url = reverse_lazy('permisos:listar') 

class DetallePermiso(DetailView):
	model = Permiso
	template_name = 'permisos/detalle.html'
	context_object_name = 'solicitud'

	def get_context_data(self, *args, **kwargs):
			context = super(DetallePermiso, self).get_context_data(**kwargs)
			context['nombreDetalle'] = 'Permiso ' + self.object.estado.__str__()
			context['botones'] = {
				'Listado de Cobros':reverse('pagos:listarCobros', args=[self.object.pk]),
				'Listado de Pagos':reverse('pagos:listarPagos', args=[self.object.pk]),
				'Eliminar Solicitud': reverse('permisos:eliminar', args=[self.object.pk])
			}
			if not isinstance(self.object.estado, Archivado):
				context['botones']['Documentación'] = reverse('permisos:listarDocumentacionPermiso', args=[self.object.pk])
				context['botones']['Nueva Acta de Inspeccion'] = reverse('actas:altaInspeccion',  args=[self.object.pk])
				context['botones']['Nueva Acta de Infraccion'] = reverse('actas:altaInfraccion',  args=[self.object.pk])
				context['botones']['Nuevo Cobro de Infraccion'] = reverse('pagos:altaCobroInfraccion', args=[self.object.pk])
				context['botones']['Nuevo Pago de Infraccion'] = reverse('pagos:AltaPagoInfraccion', args=[self.object.pk])
			if isinstance(self.object.estado, (Otorgado,Baja)):
				context['botones']['Nuevo Cobro de Canon'] = reverse('pagos:altaCobro', args=[self.object.pk])
				context['botones']['Nuevo Pago de Canon'] = reverse('pagos:altaPago', args=[self.object.pk])
			if isinstance(self.object.estado, Baja):
				context['botones']['Archivar Expediente']=reverse('documentos:archivarPermiso', args=[self.object.pk])
			if isinstance(self.object.estado, (Solicitado,Publicado,Otorgado)):
				context['botones']['Baja de Permiso'] = reverse('documentos:bajaPermiso', args=[self.object.pk]),

			context['utilizando'] = self.object.getEstados(1)[0].utilizando
			context['return_label']='Listado de Permisos'
			context['return_path']=reverse('permisos:listar')
			return context


class ListadoDocumentacionPermiso(DetailView):
	model = Permiso
	template_name = 'permisos/listadoDocuPermiso.html'
	context_object_name = 'permiso'

	def get_context_data(self, **kwargs):
		context = super(ListadoDocumentacionPermiso, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de Documentos'
		context['botones'] = {
			'Volver al detalle del Permiso': reverse('permisos:detalle', args=[self.object.pk])}
		context['documentos'] = list(context['permiso'].documentos.all())
		return context

def visar_documento_solicitud(request,pks,pkd):
	permiso = Permiso.objects.get(pk=pks)
	documento = permiso.documentos.get(pk=pkd)
	permiso.hacer('revisar',request.user, datetime.now(), [documento])
	return redirect('permisos:listarDocumentacionPermiso', pks)

def rechazar_documento_solicitud(request,pks,pkd):
	permiso = Permiso.objects.get(pk=pks)
	documento = permiso.documentos.get(pk=pkd)
	permiso.hacer('rechazar',request.user, datetime.now(), [documento])
	return redirect('permisos:listarDocumentacionPermiso', pks)
