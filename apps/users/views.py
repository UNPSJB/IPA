from django.shortcuts import render, redirect
from .models import Usuario
from .tables import UsuarioTable
from django_tables2 import SingleTableView
from apps.generales.views import GenericAltaView, GenericEliminarView
from .forms import UsuarioForm
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.views.generic.base import TemplateView

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
	cargar_otro_url = reverse_lazy('usuarios:alta')

	def get(self, request, *args, **kwargs):
		usuario_form = self.form_class()
		context = self.get_context_data()
		context['form'] = usuario_form
		return render(request, self.template_name, context=context)

	def post(self, request, *args, **kwargs):
		usuario_form = self.form_class(request.POST)
		if usuario_form.is_valid():
			try:
				usuario_form.save()
			except Exception as e:
				print('Ocurrio un error')
				print(e)
			if 'cargarOtro' in request.POST:
				return redirect(self.cargar_otro_url)
			return redirect(self.success_url)		
		else: 
			context = self.get_context_data()
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
	