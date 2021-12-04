from django.core.urlresolvers import reverse_lazy
from apps.personas.models import Empresa
from apps.personas.forms import *
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from apps.generales.views import GenericAltaView
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from django.views import View
from django_tables2.views import SingleTableView
from apps.personas.tables import EmpresaTable
from django.core.urlresolvers import reverse

class AltaEmpresa(GenericAltaView):
	model = Empresa
	form_class = EmpresaForm
	template_name = 'empresas/alta.html'
	success_url = reverse_lazy('empresas:listado')
	message_error = "Empresa existente"
	cargar_otro_url = reverse_lazy('empresas:alta')
	permission_required = 'personas.cargar_empresa'
	redirect_url = 'empresas:listado'

class DetalleEmpresa(DetailView):
	model = Empresa
	template_name = 'empresas/detalle.html'

	def get_context_data(self, **kwargs):
		context = super(DetalleEmpresa, self).get_context_data(**kwargs)
		context['nombreDetalle'] = ' Empresa'
		context['return_label'] = 'Listado Empresas'
		context['return_path']= reverse('empresas:listado')
		context['ayuda'] = 'solicitante.html#como-crear-una-nueva-empresa'
		return context

class Listado(SingleTableView):
	model = Empresa
	template_name = 'empresas/listado.html'
	table_class = EmpresaTable
	paginate_by = 12

class DataEmpresas(View):
	def get(self, request, *args, **kwargs):
		empresas = models.Empresa.objects.all()
		empresaDict = []
		for empresa in empresas:
			empresaDict.append({"razonSocial": empresa.razonSocial, "cuit": empresa.cuit})
		return JsonResponse({"data": empresaDict})

class ModificarEmpresa(UpdateView):
	model = Empresa
	form_class = EmpresaForm
	success_url = reverse_lazy('empresas:listado')
	template_name = 'empresas/alta.html'
	def get_context_data(self, **kwargs):
		context = super(ModificarEmpresa, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Detalle Empresa'
		context['return_label'] = 'Listado Empresas'
		context['return_path']= reverse('empresas:listado')
		context['ayuda'] = 'solicitante.html#como-crear-una-nueva-empresa'
		return context

class EliminarEmpresa(DeleteView):
	model = Empresa
	success_url = reverse_lazy('empresas:listado')
	
	def delete(self, request, *args, **kwargs):
		try:
			self.object = self.get_object()
			self.object.delete()

			return JsonResponse({
				"success": True
			})
		except Error as e:
			return JsonResponse({
				"success": False,
				"message": e.value()
			})