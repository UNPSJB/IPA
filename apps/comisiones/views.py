from django.shortcuts import render
from .forms import *
from apps.documentos.models import Documento
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from .models import Comision
from apps.generales.views import GenericListadoView, GenericAltaView,GenericDetalleView,GenericModificacionView,GenericEliminarView
from .tables import ComisionTable
from .filters import ComisionFilter
from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib import messages

class AltaComision(GenericAltaView):
	form_class = ComisionForm
	template_name = 'comisiones/alta.html'
	success_url = reverse_lazy('comisiones:listar')
	permission_required = 'comisiones.cargar_comision'
	redirect_url = 'comisiones:listar'

	def get_context_data(self, **kwargs):
		context = super(AltaComision, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Nueva Comisión'
		context['ayuda'] = 'comision.html'
		return context

	def post(self, request):
		comision_form = ComisionForm(request.POST)
		if comision_form.is_valid():
			comision_form.save()
			return redirect('comisiones:listar')
		return render(request, self.template_name, {'form':comision_form, 'message_error': comision_form.errors['__all__'],'empleados':comision_form.cleaned_data['empleados']})
		

class DetalleComision(GenericDetalleView):
	model = Comision
	template_name = 'comisiones/detalle.html'
	context_object_name = 'comision'
	permission_required = 'comisiones.detalle_comision'
	redirect_url = 'comisiones:listar'

	def get_context_data(self, **kwargs):
		context = super(DetalleComision, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de Comision'
		context['botones'] = {
		#'Modificar Comision': reverse('comisiones:modificar', args=[self.object.id]),
		#'Eliminar Comision': reverse('comisiones:eliminar', args=[self.object.id]),
		}
		context['return_label']='listado de Comisiones'
		context['return_path']=reverse('comisiones:listar')
		return context


class ListadoComision(GenericListadoView):
	model = Comision
	template_name = 'comisiones/listado.html'
	table_class = ComisionTable
	paginate_by = 12
	filterset_class = ComisionFilter
	export_name = 'listado_comisiones'
	permission_required = 'comisiones.listado_comision'
	redirect_url = '/'

	def get_context_data(self, **kwargs):
		context = super(ListadoComision, self).get_context_data(**kwargs)
		context['nombreReverse'] = 'comisiones'
		context['nombreLista'] = 'Listado de Comisiones'
		context['headers'] = ['Empleados', 'Localidades', 'Fecha Inicio - Fecha Fin', 'Acción', 'Detalle']
		context['url_nuevo'] = reverse('comisiones:alta')
		return context

class ModificarComision(GenericModificacionView):
	model = Comision
	form_class = ComisionForm
	template_name = 'comisiones/alta.html'
	success_url = reverse_lazy('comisiones:listar')
	permission_required = 'comisiones.modificar_comision'
	redirect_url = 'comisiones:listar'

	def post(self, request, pk):
		self.object = self.get_object
		id_comision = pk
		comision = self.model.objects.get(id=id_comision)
		form = self.form_class(request.POST, instance=comision)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		context = super(ModificarComision, self).get_context_data(**kwargs)
		context['botones'] = {
			'Nuevo Empleado': reverse('personas:alta')
			}
		context['nombreForm'] = 'Nueva Comisión'
		context['return_path'] = reverse('comisiones:listar')
		context['form'].fields['empleados'].initial = self.object.empleados.values_list('id',flat=True)
		
		return context

	def get (self, request, *args, **kwargs):
		self.object = self.get_object()
		return super(ModificarComision, self).get(request,*args,**kwargs)

class DeleteComision(GenericEliminarView):
	model = Comision
	template_name = 'delete.html'
	success_url = reverse_lazy('comisiones:listar') 
	permission_required = 'comisiones.eliminar_comision'
	redirect_url = 'comisiones:listar'

	def handle_no_permission(self):
		messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
		return redirect(self.redirect_url)

	def post(self, request, *args, **kwargs):
		if request.user.has_perm(self.permission_required):
			self.object = self.get_object()
			if len(self.object.documentos.all())>0: 
				return JsonResponse({
				"success": False,
				"message": ('error',"La Comision posee actas cargadas")
				})
			else:
				self.object.delete()
				return JsonResponse({
					"success": True,
					"message": 'Comision eliminada correctamente'
				})
		else:
			return JsonResponse({
					"success": False,
					"message": ('permiso','No posee los permisos necesarios para realizar para realizar esta operación')
			}) 