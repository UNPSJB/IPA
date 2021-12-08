from django.shortcuts import render
from ..forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from ..models import Afluente
from apps.permisos.models import Permiso
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView
from ..tables import AfluentesTable
from ..filters import AfluentesFilter
from apps.generales.views import GenericListadoView, GenericAltaView,GenericDetalleView,GenericModificacionView,GenericEliminarView
#Afluente

class AltaAfluente(GenericAltaView):
	model = Afluente
	form_class = AfluenteForm
	template_name = 'establecimientos/afluentes/alta.html'
	success_url = reverse_lazy('afluentes:listar')
	permission_required = 'afluentes.cargar_afluente'
	redirect_url = 'afluentes:listar'

	def get_context_data(self, **kwargs):
		context = super(AltaAfluente, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Nuevo Afluente'
		context['ayuda'] = 'localidad.html#como-crear-un-nuevo-afluente'
		if context['return_label'] == None:
			context['return_label'] = "listado de afluentes"
		return context

class DetalleAfluente(GenericDetalleView):
	model = Afluente
	template_name = 'establecimientos/afluentes/detalle.html'	
	context_object_name = 'afluente'
	permission_required = 'afluentes.detalle_afluente'
	redirect_url = 'afluentes:listar'

	def get_context_data(self, **kwargs):
		context = super(DetalleAfluente, self).get_context_data(**kwargs)
		context['nombreDetalle'] = ' Afluente'
		context['return_label'] = 'listado de Afluentes'
		context['return_path'] = reverse('afluentes:listar')
		return context	

class ListadoAfluentes(GenericListadoView):
	model = Afluente
	template_name = 'establecimientos/afluentes/listado.html'
	table_class = AfluentesTable
	paginate_by = 12
	filterset_class = AfluentesFilter
	export_name = 'listado_afluentes'
	permission_required = 'afluentes.listar_afluente'
	redirect_url = '/'	
	
	def get_context_data(self, **kwargs):
		context = super(ListadoAfluentes, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de Afluentes'
		context['url_nuevo'] = reverse('afluentes:alta')
		return context	

class ModificarAfluente(GenericModificacionView):
	model = Afluente
	form_class = AfluenteForm
	template_name = 'establecimientos/afluentes/alta.html'
	success_url = reverse_lazy('afluentes:listar')
	permission_required = 'afluentes.modificar_afluente'
	redirect_url = 'afluentes:listar'

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_afluente = kwargs['pk']
		afluente = self.model.objects.get(id=id_afluente)
		form = self.form_class(request.POST, instance=afluente)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		context = super(ModificarAfluente, self).get_context_data(**kwargs)
		context['return_path'] = reverse_lazy('afluentes:listar')
		context['nombreForm'] = 'Modificar Afluente'
		context['return_label'] = 'listado de Afluentes'
		return context

class DeleteAfluente(GenericEliminarView):
	model = Afluente
	permission_required = 'afluentes.eliminar_afluente'
	redirect_url = 'afluentes:listar'

	def post(self, request, *args, **kwargs):
		if request.user.has_perm(self.permission_required):
			self.object = self.get_object()
			afluentes = Permiso.objects.filter(afluente__in=[self.object.pk])
			if len(afluentes)>0: 
				return JsonResponse({
				"success": False,
				"message": ('error',"El afluente esta siendo utilizado en un permiso")
				})
			else:
				self.object.delete()
				return JsonResponse({
					"success": True,
					"message": "Afluente eliminado correctamente"
				})
		else:
			return JsonResponse({
					"success": False,
					"message": ('permiso','No posee los permisos necesarios para realizar para realizar esta operación')
			})