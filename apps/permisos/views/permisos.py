from django.urls import reverse_lazy, reverse
from ..models import Permiso, Otorgado
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
	context_object_name = 'permiso'
	

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

class DetallePermiso(DetailView):
	model = Permiso
	template_name = 'permisos/detalle.html'
	context_object_name = 'solicitud'

	def get_context_data(self, *args, **kwargs):
			context = super(DetallePermiso, self).get_context_data(**kwargs)
			context['nombreDetalle'] = self.object.estado.__str__()
			context['botones'] = {
				'Documentación': reverse('permisos:listarDocumentacionPermiso', args=[self.object.pk]),
				'Nueva Acta de Inspeccion': reverse('actas:altaInspeccion',  args=[self.object.pk]),
				'Nueva Acta de Infraccion': reverse('actas:altaInfraccion',  args=[self.object.pk]),
				'Nuevo Cobro de Infraccion':reverse('pagos:altaCobroInfraccion', args=[self.object.pk]),
				'Nuevo Pago de Infraccion':reverse('pagos:AltaPagoInfraccion', args=[self.object.pk]),
				'Listado de Cobros':reverse('pagos:listarCobros', args=[self.object.pk]),
				'Listado de Pagos':reverse('pagos:listarPagos', args=[self.object.pk]),
				'Eliminar Solicitud': reverse('permisos:eliminar', args=[self.object.pk])
			}
			if isinstance(self.object.estado, Otorgado):
				for e in funciones_otorgado(self.object.pk):
					context['botones'][e[0]]=e[1]
			context['utilizando'] = self.object.getEstados(1)[0].utilizando
			context['return_label']='Listado de Permisos'
			context['return_path']=reverse('permisos:listar')
			return context

def funciones_otorgado(pk):
	return [('Nuevo Cobro de Canon',reverse('pagos:altaCobro', args=[pk])),
			('Nuevo Pago de Canon',reverse('pagos:altaPago', args=[pk]))]

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

class NuevaDocumentacionRequerida(AltaDocumento):
	def get_form(self, form_class):
		form  = self_form_class()
		permiso = Permiso.objects.get(id= self.permiso.pk)
		
		return form 
