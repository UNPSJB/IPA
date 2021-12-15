from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from ..models import Solicitado, Publicado, Permiso, Otorgado, Baja, Archivado
from ..forms import PermisoForm, SolicitadoForm
from django.views.generic import ListView,DeleteView,DetailView,UpdateView
from django.shortcuts import redirect
from django.views import View
from datetime import date, datetime
from apps.documentos.views import AltaDocumento
from apps.generales.views import GenericListadoView, GenericAltaView,GenericEliminarView,GenericModificacionView,GenericDetalleView
from ..tables import PermisosTable
from ..filters import PermisosFilter
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib import messages as Messages

class ListadoPermisos(GenericListadoView):
	model = Permiso
	template_name = 'permisos/listado.html'
	table_class = PermisosTable
	paginate_by = 8
	filterset_class = PermisosFilter
	context_object_name = 'permiso'
	export_name = 'listado_permisos'
	permission_required = 'permisos.listar_permiso'
	redirect_url = '/'

	def get_context_data(self, **kwargs):
		context = super(ListadoPermisos, self).get_context_data(**kwargs)
		context['url_nuevo'] = reverse('permisos:alta')
		return context

class AltaPermiso(GenericAltaView):
	model = Permiso
	form_class = PermisoForm
	template_name = 'permisos/alta.html'
	success_url = reverse_lazy('permisos:listar')
	message_error = ["Permiso existente"]
	cargar_otro_url = reverse_lazy('permiso:alta')
	permission_required = 'permisos.cargar_permiso'
	redirect_url = 'permisos:listar'

	def get_context_data(self, **kwargs):
		context = super(AltaPermiso, self).get_context_data(**kwargs)
		context['solicitadoForm'] = SolicitadoForm()
		context['ayuda'] = 'solicitud.html#como-crear-un-nuevo-permiso'
		context['nombreForm'] = "Nuevo Permiso"
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
		return render(request, self.template_name, {'form':permiso_form,'solicitadoForm':solicitado_form})

class ModificarPermiso(GenericModificacionView):
	model = Permiso
	form_class = PermisoForm
	template_name = 'permisos/alta.html'
	success_url = reverse_lazy('permisos:listar')
	permission_required = 'permisos.modificar_permiso'
	redirect_url = 'permisos:listar'

	
	def get_context_data(self, **kwargs):
		context = super(ModificarPermiso, self).get_context_data(**kwargs)
		context['nombreForm'] = "Modificar Permiso"
		context['solicitadoForm'] = SolicitadoForm(instance=self.permiso.estado)
		context['ayuda'] = 'solicitud.html#como-crear-un-nuevo-permiso'
		context['return_path'] = reverse('permisos:listar')
		return context
	
	def get(self, request, *args, **kwargs):
		self.permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		if (len(self.permiso.documentos.all())>0 or len(self.permiso.pagos.all())>0 or len(self.permiso.cobros.all())>0):
			Messages.error(self.request, "El permiso posee Documentos / Cobros / Pagos por ello no se puede modificar sus datos")
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso.pk]))
		
		return super(ModificarPermiso,self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_permiso = kwargs['pk']
		self.permiso = self.model.objects.get(pk=id_permiso)
		permiso_form = self.form_class(request.POST,instance=self.permiso)
		solicitado_form = SolicitadoForm(request.POST,instance=self.permiso.estado)
		print(request.POST)
		print(solicitado_form)
		if permiso_form.is_valid() and solicitado_form.is_valid():
			permiso = permiso_form.save(commit=False)
			permiso.fechaSolicitud = solicitado_form.data['fecha']
			permiso = permiso_form.save()
			solicitado = solicitado_form.save(commit=False)
			solicitado.permiso = permiso
			solicitado.usuario = request.user
			solicitado.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			context = self.get_context_data(form=permiso_form)
			context['solicitadoForm'] = solicitado_form
			return render(request, self.template_name, context)





#class PermisoDelete(DeleteView):
class PermisoDelete(LoginRequiredMixin,DeleteView):
	model = Permiso
	template_name = 'delete.html'
	success_url = reverse_lazy('permisos:listar')
	permission_required = 'permisos.eliminar_permiso'

	def get(self, request, *args, **kwargs):
		self.permiso = Permiso.objects.get(pk=kwargs.get('pk'))
		if not request.user.has_perm(self.permission_required):
			Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
			return HttpResponseRedirect(reverse('permisos:detalle', args=[self.permiso.pk]))

		return super(PermisoDelete,self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		if request.user.has_perm(self.permission_required):
			self.permiso = Permiso.objects.get(pk=kwargs.get('pk'))
			if (len(self.permiso.documentos.all())>0 or len(self.permiso.pagos.all())>0 or len(self.permiso.cobros.all())>0):
				return JsonResponse({
				"success": False,
				"message": ('error',"El permiso posee Documentos / Cobros / Pagos")
				})
			else:
				self.permiso.delete()
				return JsonResponse({
					"success": True,
					"message": 'Comision eliminada correctamente'
				})
		else:
			return JsonResponse({
					"success": False,
					"message": ('permiso','No posee los permisos necesarios para realizar para realizar esta operación')
			}) 

class DetallePermiso(GenericDetalleView):
	model = Permiso
	template_name = 'permisos/detalle.html'
	context_object_name = 'solicitud'
	permission_required = 'permisos.detalle_permiso'
	redirect_url = 'permisos:listar'

	def get_context_data(self, *args, **kwargs):
			context = super(DetallePermiso, self).get_context_data(**kwargs)
			context['nombreDetalle'] = 'Permiso '
			context['botones'] = {
				'Listado de Cobros':reverse('pagos:listarCobros', args=[self.object.pk]),
				'Listado de Pagos':reverse('pagos:listarPagos', args=[self.object.pk]),
				#'Eliminar Solicitud': reverse('permisos:eliminar', args=[self.object.pk])
			}
			if not isinstance(self.object.estado, Archivado):
				context['botones']['Documentación'] = reverse('permisos:listarDocumentacionPermiso', args=[self.object.pk])
				context['botones']['Nueva Acta de Inspeccion'] = reverse('actas:altaInspeccion',  args=[self.object.pk])
				context['botones']['Nueva Acta de Infraccion'] = reverse('actas:altaInfraccion',  args=[self.object.pk])
			if isinstance(self.object.estado, Baja):
				context['botones']['Archivar Expediente']=reverse('documentos:archivarPermiso', args=[self.object.pk])
			if isinstance(self.object.estado, (Solicitado,Publicado,Otorgado)):
				context['botones']['Baja de Permiso'] = reverse('documentos:bajaPermiso', args=[self.object.pk])

			context['utilizando'] = self.object.getEstados(1)[0].utilizando
			context['return_label']='Listado de Permisos'
			context['return_path']=reverse('permisos:listar')
			context['solicitado'] = self.object.getEstados(1)[0]
			return context


class ListadoDocumentacionPermiso(GenericDetalleView):
	model = Permiso
	template_name = 'permisos/listadoDocuPermiso.html'
	context_object_name = 'permiso'
	permission_required = 'permisos.listar_documentacion_presentada'
	redirect_url = 'permisos:listar'

	def get_context_data(self, **kwargs):
		context = super(ListadoDocumentacionPermiso, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de Documentos'
		context['botones'] = {
			'Volver al detalle del Permiso': reverse('permisos:detalle', args=[self.object.pk])}
		context['documentos'] = list(context['permiso'].documentos.all())
		return context

@permission_required('permisos.visar_documentacion_solicitud', login_url="/permisos/listar")
def visar_documento_solicitud(request,pks,pkd):
	permiso = Permiso.objects.get(pk=pks)
	documento = permiso.documentos.get(pk=pkd)
	permiso.hacer('revisar',request.user, datetime.now(), [documento])
	return redirect('permisos:listarDocumentacionPermiso', pks)

@permission_required('permisos.rechazar_documentacion_solicitud', login_url="/permisos/listar")
def rechazar_documento_solicitud(request,pks,pkd):
	permiso = Permiso.objects.get(pk=pks)
	documento = permiso.documentos.get(pk=pkd)
	permiso.hacer('rechazar',request.user, datetime.now(), [documento])
	return redirect('permisos:listarDocumentacionPermiso', pks)
