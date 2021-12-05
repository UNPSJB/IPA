from django.shortcuts import render, redirect
from .models import Usuario
from .tables import UsuarioTable
from django_tables2 import SingleTableView
from apps.generales.views import GenericDetalleView,GenericModificacionView
from django.views.generic import DeleteView
from .forms import UsuarioForm
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.db.utils import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib import messages as Messages
from django.http import JsonResponse

class ListadoUsuarios(LoginRequiredMixin,PermissionRequiredMixin,SingleTableView):
	model = Usuario
	template_name = 'usuarios/listado.html'
	table_class = UsuarioTable
	table_data = Usuario.usuarios.all()
	paginate_by = 12
	permission_required = 'usuarios.listar_usuarios'
	redirect_url = '/'

	def handle_no_permission(self):
		Messages.error(self.request, 'No posee los necesarios para realizar permisos para realizar esta operación')
		return redirect(self.redirect_url)

class NuevoUsuario(LoginRequiredMixin,PermissionRequiredMixin,TemplateView):
	model = Usuario
	form_class = UsuarioForm
	template_name = 'usuarios/alta.html'
	success_url = reverse_lazy('usuarios:listado')
	permission_required = 'usuarios.cargar_usuario'
	redirect_url = 'usuarios:listado'

	def handle_no_permission(self):
		Messages.error(self.request, 'No posee los necesarios para realizar permisos para realizar esta operación')
		return redirect(self.redirect_url)

	def get(self, request, *args, **kwargs):
		usuario_form = self.form_class()
		context = self.get_context_data()
		context['form'] = usuario_form
		context['return_path'] = reverse_lazy('usuarios:listado')
		return render(request, self.template_name, context=context)

	def post(self, request, *args, **kwargs):
		usuario_form = self.form_class(request.POST)
		context = self.get_context_data()
		if usuario_form.is_valid():
			try:
				usuario_form.save()
			except IntegrityError as e:
				context['message_error'] = 'El nombre de usuario ya existe. Por favor, seleccione otro.'
				context['form'] = usuario_form
				return render(request, self.template_name, context=context)
			except Exception as e:
				context['message_error'] = str(e)
				context['form'] = usuario_form
				return render(request, self.template_name, context=context)
			if 'cargarOtro' in request.POST:
				context['message_success'] = 'El usuario {} ha sido agregado exitosamente.'.format(usuario_form.cleaned_data.get('username'))
				context['form'] = self.form_class()
				return render(request, self.template_name, context=context)
			return redirect(self.success_url)		
		else: 
			
			context['form'] = usuario_form
			return render(request, self.template_name, context=context)

class DetalleUsuario(GenericDetalleView):
	model = Usuario
	template_name = 'usuarios/detalle.html'
	permission_required = 'usuarios.detalle_usuario'
	redirect_url = 'usuarios:listado'

	def get_context_data(self, **kwargs):
		context = super(DetalleUsuario, self).get_context_data(**kwargs)
		context['nombreDetalle'] = 'Detalle Usuario'
		context['return_label'] = 'listado de Usuarios'
		context['return_path']= reverse('usuarios:listado')
		return context

class ModificarUsuario(GenericModificacionView):
	model = Usuario
	form_class = UsuarioForm
	success_url = reverse_lazy('usuarios:listado')
	template_name = 'usuarios/alta.html'
	permission_required = 'usuarios.modificar_usuario'
	redirect_url = 'usuarios:listado'

class EliminarUsuario(LoginRequiredMixin,DeleteView):
	model = Usuario
	success_url = reverse_lazy('usuarios:listado')
	permission_required = 'usuarios.eliminar_usuario'

	def delete(self, request, *args, **kwargs):
		if not request.user.has_perm(self.permission_required):
			return JsonResponse({"success": False,"message": ('permiso',"No posee los necesarios para realizar permisos para realizar esta operación")})
		try:
			self.object = self.get_object()
			self.object.delete()

			return JsonResponse({
				"success": True
			})
		except Exception as e:
			return JsonResponse({
				"success": False,
				"message": ('error',"No se pudo eliminar este usuario")
			})
	