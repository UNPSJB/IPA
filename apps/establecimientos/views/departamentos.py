from django.shortcuts import render
from ..forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from ..models import Departamento
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView

from apps.generales.views import GenericListadoView, GenericAltaView,GenericModificacionView,GenericDetalleView,GenericEliminarView
from ..tables import DepartamentosTable
from ..filters import DepartamentosFilter
#Departamento

class AltaDepartamento(GenericAltaView):
	model = Departamento
	form_class = DepartamentoForm
	template_name = 'establecimientos/departamentos/alta.html'
	success_url = reverse_lazy('departamentos:listar')
	permission_required = 'establecimientos.cargar_departamento'
	redirect_url = 'departamentos:listar'

	def get_context_data(self, **kwargs):
		context = super(AltaDepartamento, self).get_context_data(**kwargs)
		context['nombreForm'] = "Nuevo Departamento"
		context['return_path'] = reverse('departamentos:listar')
		context['ayuda'] = 'localidad.html#como-crear-un-nuevo-departamento'
		return context

class ModificarDepartamento(GenericModificacionView):
	model = Departamento
	form_class = DepartamentoForm
	template_name = 'establecimientos/departamentos/alta.html'
	success_url = reverse_lazy('departamentos:listar')
	permission_required = 'establecimientos.modificar_departamento'
	redirect_url = 'departamentos:listar'

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_departamento = kwargs['pk']
		departamento = self.model.objects.get(id=id_departamento)
		form = self.form_class(request.POST, instance=departamento)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		context = super(ModificarDepartamento, self).get_context_data(**kwargs)
		context['nombreForm'] = "Modificar Departamento"
		context['return_path'] = reverse('departamentos:listar')
		return context

class DetalleDepartamento(GenericDetalleView):
	model = Departamento
	template_name = 'establecimientos/departamentos/detalle.html'		
	context_object_name = 'departamento'
	permission_required = 'establecimientos.detalle_departamento'
	redirect_url = 'departamentos:listar'

	def get_context_data(self, **kwargs):
		context = super(DetalleDepartamento, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de Departamento'
		context['return_label'] = 'listado de Departamentos'
		context['return_path'] = reverse('departamentos:listar')
		return context

class ListadoDepartamentos(GenericListadoView):
	model = Departamento	
	template_name = 'establecimientos/departamentos/listado.html'
	table_class = DepartamentosTable
	paginate_by = 12
	filterset_class = DepartamentosFilter
	export_name = 'listado_departamentos'
	context_object_name = 'departamentos'
	permission_required = 'establecimientos.listar_departamento'
	redirect_url = '/'

	def get_context_data(self, **kwargs):
		context = super(ListadoDepartamentos, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Listado de Departamentos'
		context['url_nuevo'] = reverse('departamentos:alta')
		return context

class DeleteDepartamento(GenericEliminarView):
	model = Departamento
	template_name = 'delete.html'
	success_url = reverse_lazy('departamentos:listar')
	permission_required = 'establecimientos.eliminar_departamento'

	def post(self, request, *args, **kwargs):
		if request.user.has_perm(self.permission_required):
			self.object = self.get_object()
			localidades = Localidad.objects.filter(departamento__in=[self.object.pk])
			if len(localidades)>0: 
				return JsonResponse({
				"success": False,
				"message": ('error',"El Departamento esta siendo utilizado en una localidad")
				})
			else:
				self.object.delete()
				return JsonResponse({
					"success": True,
					"message": "Departamento eliminado correctamente"
				})
		else:
			return JsonResponse({
					"success": False,
					"message": ('permiso','No posee los permisos necesarios para realizar para realizar esta operación')
			})
