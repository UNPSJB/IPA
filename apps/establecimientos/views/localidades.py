from django.shortcuts import render
from ..forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from ..models import Localidad
from apps.generales.views import GenericAltaView, GenericListadoView,GenericModificacionView,GenericEliminarView
from ..tables import LocalidadesTable
from ..filters import LocalidadesFilter

#Localidad

class AltaLocalidad(GenericAltaView):
	model = Localidad
	form_class = LocalidadForm
	template_name = 'establecimientos/localidades/alta.html'
	success_url = reverse_lazy('localidades:listar')
	permission_required = 'localidades.cargar_localidad'
	redirect_url = 'localidades:listar'

	def get_context_data(self, **kwargs):
		context = super(AltaLocalidad, self).get_context_data(**kwargs) 
		context['nombreForm'] = 'Nueva Localidad'
		context['ayuda'] = 'localidad.html#como-crear-una-nueva-localidad'
		return context

class ModificarLocalidad(GenericModificacionView):
	model = Localidad
	form_class = LocalidadForm
	template_name = 'establecimientos/localidades/alta.html'
	success_url = reverse_lazy('localidades:listar')
	permission_required = 'localidades.modificar_localidad'
	redirect_url = 'localidades:listar'

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_localidad = kwargs['pk']
		localidad = self.model.objects.get(id=id_localidad)
		form = self.form_class(request.POST, instance=localidad)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		context = super(ModificarLocalidad, self).get_context_data(**kwargs)
		context['nombreForm'] = "Modificar Localidad"
		context['return_path'] = reverse('localidades:listar')
		return context


class ListadoLocalidades(GenericListadoView):
	model = Localidad
	template_name = 'establecimientos/localidades/listado.html'
	table_class = LocalidadesTable
	paginate_by = 20
	filterset_class = LocalidadesFilter
	export_name = 'listado_localidades'
	permission_required = 'localidades.listar_localidad'
	redirect_url = '/'

	def get_context_data(self, **kwargs):
		context = super(ListadoLocalidades, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de Localidades'
		context['nombreReverse'] = 'localidades'
		context['headers'] = ['Código Postal', 'Nombre','Departamento']
		context['url_nuevo'] = reverse('localidades:alta')
		return context

class LocalidadDelete(GenericEliminarView):
	model = Localidad
	permission_required = 'localidades.eliminar_localidad'

	def post(self, request, *args, **kwargs):
		if request.user.has_perm(self.permission_required):
			self.object = self.get_object()
			establecimientos = Establecimiento.objects.filter(localidad__in=[self.object.pk])
			if len(establecimientos)>0: 
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