from django.shortcuts import render
from ..forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from ..models import Establecimiento
from apps.permisos.models import Permiso
from apps.generales.views import GenericAltaView, GenericListadoView,GenericDetalleView,GenericModificacionView,GenericEliminarView
from ..tables import EstablecimientosTable
from ..filters import EstablecimientosFilter

# Establecimiento
class AltaEstablecimiento(GenericAltaView):
	model = Establecimiento
	form_class = EstablecimientoForm
	template_name = 'establecimientos/alta.html'
	success_url = reverse_lazy('establecimientos:listar')
	permission_required = 'establecimientos.cargar_establecimiento'
	redirect_url = 'establecimientos:listar'

	def get_context_data(self, **kwargs):
		context = super(AltaEstablecimiento, self).get_context_data(**kwargs)
		context['botones'] = {
			'Nuevo Dueño': reverse('personas:alta'),
			}
		context['nombreForm'] = "Nuevo Establecimiento"
		context['ayuda'] = 'solicitante.html#como-crear-un-nuevo-establecimiento'
		if context['return_label'] == None:
			context['return_label'] = "listado de Establecimientos"
		return context

class ListadoEstablecimientos(GenericListadoView):
	model = Establecimiento
	template_name = 'establecimientos/listado.html'
	table_class = EstablecimientosTable
	paginate_by = 20
	filterset_class = EstablecimientosFilter
	context_object_name = 'establecimientos'
	export_name = 'listado_establecimientos'
	permission_required = 'establecimientos.listar_establecimiento'
	redirect_url = '/'

	def get_context_data(self, **kwargs):
		context = super(ListadoEstablecimientos, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de Establecimientos'
		return context

class DetalleEstablecimiento(GenericDetalleView):
	model = Establecimiento
	template_name = 'establecimientos/detalle.html'
	context_object_name = 'establecimiento'
	permission_required = 'establecimientos.detalle_establecimiento'
	redirect_url = 'establecimientos:listar'

	def get_context_data(self, **kwargs):
		context = super(DetalleEstablecimiento, self).get_context_data(**kwargs)
		context['nombreDetalle'] = ' Establecimiento'
		context['return_label'] = 'listado de Establecimientos'
		context['return_path'] = reverse('establecimientos:listar')
		return context

class ModificarEstablecimiento(GenericModificacionView):
	model = Establecimiento
	form_class = EstablecimientoChange
	template_name = 'establecimientos/alta.html'
	success_url = reverse_lazy('establecimientos:listar')
	permission_required = 'establecimientos.modificar_establecimiento'
	redirect_url = 'establecimientos:listar'

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_establecimiento = kwargs['pk']
		establecimiento = self.model.objects.get(codigoCatastral=id_establecimiento)
		form = self.form_class(request.POST, instance=establecimiento)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		context = super(ModificarEstablecimiento, self).get_context_data(**kwargs)
		context['nombreForm'] = "Modificar Establecimiento"
		context['return_label'] = 'listado de Establecimientos'
		context['return_path'] = reverse('establecimientos:listar')
		return context


class DeleteEstablecimiento(GenericEliminarView):
	model = Establecimiento
	permission_required = 'establecimientos.eliminar_establecimiento'

	def post(self, request, *args, **kwargs):
		if request.user.has_perm(self.permission_required):
			self.object = self.get_object()
			permisos = Permiso.objects.filter(establecimiento__in=[self.object.pk])
			if len(permisos)>0: 
				return JsonResponse({
				"success": False,
				"message": ('error',"El Establecimiento esta siendo utilizado en un permiso")
				})
			else:
				self.object.delete()
				return JsonResponse({
					"success": True,
					"message": 'Establecimiento eliminado correctamente'
				})
		else:
			return JsonResponse({
					"success": False,
					"message": ('permiso','No posee los permisos necesarios para realizar para realizar esta operación')
			})