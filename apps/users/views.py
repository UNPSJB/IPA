from django.shortcuts import render, redirect
from .models import Usuario
from .tables import UsuarioTable
from django_tables2 import SingleTableView
from apps.generales.views import GenericAltaView, GenericEliminarView
from .forms import UsuarioForm
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.views.generic.base import TemplateView
from django.db.utils import IntegrityError

class ListadoUsuarios(SingleTableView):
	model = Usuario
	template_name = 'usuarios/listado.html'
	table_class = UsuarioTable
	table_data = Usuario.usuarios.all()
	paginate_by = 12

class NuevoUsuario(TemplateView):
	model = Usuario
	form_class = UsuarioForm
	template_name = 'usuarios/alta.html'
	success_url = reverse_lazy('usuarios:listado')

	def get(self, request, *args, **kwargs):
		usuario_form = self.form_class()
		context = self.get_context_data()
		context['form'] = usuario_form
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

class ModificarUsuario(UpdateView):
	model = Usuario
	form_class = UsuarioForm
	success_url = reverse_lazy('usuarios:listado')
	template_name = 'usuarios/alta.html'

class EliminarUsuario(GenericEliminarView):
	model = Usuario
	success_url = reverse_lazy('usuarios:listado')
	