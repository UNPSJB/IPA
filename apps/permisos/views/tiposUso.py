from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import JsonResponse
from ..models import TipoUso
from ..forms import TipoDeUsoForm
from ..forms import *
from django.views.generic import ListView,CreateView,DeleteView,DetailView, UpdateView
from django.http import HttpResponseRedirect

from apps.generales.views import GenericListadoView, GenericAltaView

from ..tables import TipoDeUsoTable
from ..filters import TipoDeUsoFilter

# Create your views here.
class AltaTipoDeUso(GenericAltaView):
	model = TipoUso
	form_class = TipoDeUsoForm
	template_name = 'permisos/tipoDeUso/alta.html'
	success_url = reverse_lazy('tiposDeUso:listar')
	
	def get_context_data(self, **kwargs):
		context = super(AltaTipoDeUso, self).get_context_data(**kwargs)
		context['botones'] = {
			'Nuevo Documento': reverse('tipoDocumentos:alta'),
			}
		context['nombreForm'] = 'Nuevo Tipo de Uso'
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		medida = int(request.POST['medida'])
		tipoModulo = int(request.POST['tipo_modulo'])
		tipoUsoForm = self.form_class(request.POST)
		
		if tipoUsoForm.is_valid():
			if ((medida==6) and (tipoModulo == 2)):
				tipoUso = tipoUsoForm.save()
				return HttpResponseRedirect(self.get_success_url())
			elif (medida != 6) and (tipoModulo != 2):
				tipoUso = tipoUsoForm.save()
				return HttpResponseRedirect(self.get_success_url())
			else:
				return render(request, self.template_name, {'form':tipoUsoForm, 'botones':{'Nuevo Documento': reverse('tipoDocumentos:alta')}, 'nombreForm':'Nuevo Tipo de Uso',
			'message_error':['Error en la carga entre la medida y el tipo de modulo, solo se puede utilizar kw con uso energetico']})
		else:
			return render(request, self.template_name, {'form':tipoUsoForm, 'botones':{'Nuevo Documento': reverse('tipoDocumentos:alta')}, 'nombreForm':'Nuevo Tipo de Uso',
			'message_error':['Error en la carga entre la medida y el tipo de modulo, solo se puede utilizar kw con uso energetico']})

class DetalleTipoDeUso(DetailView):
	model = TipoUso
	template_name = 'permisos/tipoDeUso/detalle.html'		
	context_object_name = 'tipo'
	
	def get_context_data(self, **kwargs):
		context = super(DetalleTipoDeUso, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de Tipo de Uso'
		context['botones'] = {
			'Nuevo Tipo de Uso': reverse('tiposDeUso:alta'),
			'Modificar Tipo de Uso': reverse('tiposDeUso:modificar', args=[self.object.id]),
		}
		context['return_label'] = 'listado de Tipos de Usos'
		context['return_path'] = reverse('tiposDeUso:listar')
		return context

class ListadoTiposDeUso(GenericListadoView):
	model = TipoUso
	template_name = 'permisos/tipoDeUso/listado.html'
	table_class = TipoDeUsoTable
	paginate_by = 12
	filterset_class = TipoDeUsoFilter
	context_object_name = 'tiposDeUso'

	def get_context_data(self, **kwargs):
		context = super(ListadoTiposDeUso, self).get_context_data(**kwargs)
		context['nombreListado'] = "Listado de Tipos de Uso"
		context['botones'] = {
			'Nuevo Tipo de Uso': reverse('tiposDeUso:alta') 
			}
		return context

class DeleteTipoDeUso(DeleteView):
	model = TipoUso
	template_name = 'delete.html'
	success_url = reverse_lazy('tiposDeUso:listar')

def eliminar_tipo_de_uso(request, pk):
	permisos = Permiso.objects.filter(tipo=pk)
	if len(permisos)>0:
		return JsonResponse({
				"success": False,
				"message": "Existen otros permisos que estan usando el Tipo de Uso"
		})
	else:
		tipo = TipoUso.objects.get(pk=pk)
		tipo.delete()
		return JsonResponse({
				"success": True,
				"message": "Tipo de Uso eliminado con exito"
		})


class ModificarTipoDeUso(UpdateView):
	model = TipoUso
	form_class = TipoDeUsoForm
	template_name = 'permisos/tipoDeUso/alta.html'
	success_url = reverse_lazy('tiposDeUso:listar')

	def post(self, request, pk):
		self.object = self.get_object
		id_tipoDeUso = pk
		tipoDeUso = self.model.objects.get(id=id_tipoDeUso)
		form = self.form_class(request.POST, instance=tipoDeUso)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		context = super(ModificarTipoDeUso, self).get_context_data(**kwargs)
		context['nombreForm'] = "Modificar Tipo de Uso"
		context['botones'] = {
			'Nuevo Documento': reverse('tipoDocumentos:alta'),
			}
		context['return_path'] = reverse('tiposDeUso:listar')
		return context