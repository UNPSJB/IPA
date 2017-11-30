from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy, reverse
from ..models import TipoUso
from ..forms import TipoDeUsoForm
from ..forms import *
from django.views.generic import ListView,CreateView,DeleteView,DetailView, UpdateView
from django.http import HttpResponseRedirect



# Create your views here.
class AltaTipoDeUso(CreateView):
	model = TipoUso
	form_class = TipoDeUsoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('tiposDeUso:listar')
	
	def get_context_data(self, **kwargs):
		context = super(AltaTipoDeUso, self).get_context_data(**kwargs)
		context['botones'] = {
			'Ir a Listado': reverse('tiposDeUso:listar'),
			'Nuevo Documento': reverse('tipoDocumentos:alta'),
			}
		context['nombreForm'] = 'Nuevo Tipo de Uso'
		return context

	def post(self, request, *args, **kwargs):
		medida = int(request.POST['medida'])
		tipoModulo = int(request.POST['tipo_modulo'])
		
		if ((medida==6) and (tipoModulo == 2)) or ((medida != 6) and (tipoModulo == 1)):
			return super(AltaTipoDeUso, self).get(request,*args,**kwargs)
		return render(request, self.template_name, {'form':self.form_class, 'botones':'', 'nombreForm':'Nuevo Tipo de Uso',
			'message':'Error en la carga entre la medida y el tipo de modulo, solo se puede utilizar kw con uso energetico'})

class DetalleTipoDeUso(DetailView):
	model = TipoUso
	template_name = 'tipoDeUso/detalle.html'		
	context_object_name = 'tipo'
	
	def get_context_data(self, **kwargs):
		context = super(DetalleTipoDeUso, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle de Tipo de Uso'
		context['botones'] = {
			'Ir a Listado': reverse('tiposDeUso:listar'),
			'Nuevo Tipo de Uso': reverse('tiposDeUso:alta'),
			'Modificar Tipo de Uso': reverse('tiposDeUso:modificar', args=[self.object.id]),
			'Eliminar Tipo de Uso': reverse('tiposDeUso:eliminar', args=[self.object.id]),
			'Salir': reverse('index')
		}
		return context

class ListadoTiposDeUso(ListView):
	model = TipoUso
	template_name = 'tipoDeUso/listado.html'
	context_object_name = 'tiposDeUso'

	def get_context_data(self, **kwargs):
		context = super(ListadoTiposDeUso, self).get_context_data(**kwargs)
		context['nombreLista'] = "Listado de Tipos de Uso"
		context['nombreReverse'] = "tiposDeUso"
		context['headers'] = ['Nombre', 'Coeficiente', 'Periodo']
		context['botones'] = {
			'Nuevo Tipo de Uso': reverse('tiposDeUso:alta') 
			}
		return context

class DeleteTipoDeUso(DeleteView):
	model = TipoUso
	template_name = 'delete.html'
	success_url = reverse_lazy('tiposDeUso:listar')

class ModificarTipoDeUso(UpdateView):
	model = TipoUso
	form_class = TipoDeUsoForm
	template_name = 'forms.html'
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
			'Ir a Listado': reverse('tiposDeUso:listar'),
			'Nuevo Documento': reverse('tipoDocumentos:alta'),
			}
		return context