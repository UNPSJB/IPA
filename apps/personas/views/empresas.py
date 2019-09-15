from django.core.urlresolvers import reverse_lazy
from apps.personas import models as pmodels
from apps.personas.forms import *
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from apps.generales.views import GenericAltaView
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from django.views import View

class AltaEmpresa(GenericAltaView):
	model = pmodels.Empresa
	form_class = EmpresaForm
	template_name = 'empresas/alta.html'
	success_url = reverse_lazy('personas:listado')
	message_error = "Empresa existente"
	cargar_otro_url = reverse_lazy('empresas:alta')

class DataEmpresas(View):
	def get(self, request, *args, **kwargs):
		empresas = pmodels.Empresa.objects.all()
		empresaDict = []
		for empresa in empresas:
			empresaDict.append({"razonSocial": empresa.razonSocial, "cuit": empresa.cuit})
		return JsonResponse({"data": empresaDict})
