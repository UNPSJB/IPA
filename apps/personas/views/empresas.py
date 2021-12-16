from django.core.urlresolvers import reverse_lazy
from apps.personas.models import Empresa
from apps.personas.forms import *
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from apps.generales.views import GenericAltaView,GenericDetalleView,GenericModificacionView,GenericListadoView
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views import View
from django_tables2.views import SingleTableView
from apps.personas.tables import EmpresaTable
from django.core.urlresolvers import reverse
from django.contrib import messages as Messages
from django.shortcuts import redirect
from django.shortcuts import render
from ..tables import EmpresaFilter


class AltaEmpresa(GenericAltaView):
	model = Empresa
	form_class = EmpresaForm
	template_name = 'empresas/alta.html'
	success_url = reverse_lazy('empresas:listado')
	message_error = "Empresa existente"
	cargar_otro_url = reverse_lazy('empresas:alta')
	permission_required = 'personas.cargar_empresa'
	redirect_url = 'empresas:listado'

	def get_context_data(self,*args, **kwargs):
		context = super(AltaEmpresa, self).get_context_data(**kwargs) 
		return self.get_context_empresa(context)

	def get_context_empresa(self,context):
		context['nombreForm'] = 'Nueva Empresa'
		context['ayuda'] = 'solicitante.html#como-crear-una-nueva-empresa'
		context['return_label'] = "listado de empresas"
		return context

	def post(self, request, *args, **kwargs):
		empresa_form = self.form_class(request.POST)
		if empresa_form.is_valid():
			empresa_form.save()
			return redirect('afluentes:listar')
		return render(request, self.template_name,self.get_context_departamento({'form':empresa_form}))

class DetalleEmpresa(GenericDetalleView):
	model = Empresa
	template_name = 'empresas/detalle.html'
	permission_required = 'personas.detalle_empresa'
	redirect_url = 'empresas:listado'

	def get_context_data(self, **kwargs):
		context = super(DetalleEmpresa, self).get_context_data(**kwargs)
		context['nombreDetalle'] = ' Empresa'
		context['return_label'] = 'Listado Empresas'
		context['return_path']= reverse('empresas:listado')
		return context


class Listado(GenericListadoView):
	model = Empresa
	template_name = 'empresas/listado.html'
	table_class = EmpresaTable
	filterset_class = EmpresaFilter
	paginate_by = 10
	export_name = 'listado_empresas'
	exclude_columns = 'acciones'
	permission_required = 'personas.listar_empresa'
	redirect_url = '/'

	def handle_no_permission(self):
		Messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
		return redirect(self.redirect_url)

	def get_context_data(self, **kwargs):
		context = super(Listado, self).get_context_data(**kwargs)
		context['url_nuevo'] = reverse('empresas:alta')
		return context

class DataEmpresas(View):
	def get(self, request, *args, **kwargs):
		empresas = Empresa.objects.all()
		empresaDict = []
		for empresa in empresas:
			empresaDict.append({"Razón Social": empresa.razonSocial, "cuit": empresa.cuit})
		return JsonResponse({"data": empresaDict})

class ModificarEmpresa(GenericModificacionView):
	model = Empresa
	form_class = EmpresaForm
	success_url = reverse_lazy('empresas:listado')
	template_name = 'empresas/alta.html'
	permission_required = 'personas.modificar_empresa'
	redirect_url = 'empresas:listado'
	
	def get_context_data(self, **kwargs):
		context = super(ModificarEmpresa, self).get_context_data(**kwargs)
		context['nombreForm'] = 'Modificar Empresa'
		context['return_label'] = 'Listado Empresas'
		context['return_path']= reverse('empresas:listado')
		context['ayuda'] = 'solicitante.html#como-crear-una-nueva-empresa'
		context['form'].fields["representantes"].disabled = True
		return context

class EliminarEmpresa(LoginRequiredMixin, DeleteView):
	model = Empresa
	success_url = reverse_lazy('empresas:listado')
	permission_required = 'personas.eliminar_empresa'
	
	def delete(self, request, *args, **kwargs):
		if not request.user.has_perm(self.permission_required):
			return JsonResponse({"success": False,"message": ('permiso',"No posee los permisos necesarios para realizar esta operación")})
		try:
			self.object = self.get_object()
			self.object.delete()

			return JsonResponse({
				"success": True
			})
		except Error as e:
			return JsonResponse({
				"success": False,
				"message": ('error',"No se pudo eliminar la empresa")
			})