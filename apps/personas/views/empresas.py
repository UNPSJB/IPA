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

class AltaEmpresa(GenericAltaView):
	model = Empresa
	form_class = EmpresaForm
	template_name = 'empresas/alta.html'
	success_url = reverse_lazy('empresas:listado')
	message_error = "Empresa existente"
	cargar_otro_url = reverse_lazy('empresas:alta')

class DetalleEmpresa(DetailView):
	model = Empresa
	template_name = 'empresas/detail.html'

class Listado(SingleTableView):
	model = Empresa
	template_name = 'empresas/listado.html'
	table_class = EmpresaTable
	paginate_by = 12


class ModificarEmpresa(UpdateView):
	model = Empresa
	form_class = EmpresaForm
	success_url = reverse_lazy('empresas:listado')
	template_name = 'empresas/alta.html'

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