from django.shortcuts import render
from .models import Usuario
from .tables import UsuarioTable
from django_tables2 import SingleTableView
from apps.generales.views import GenericAltaView, GenericEliminarView
from .forms import UsuarioForm
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView


class ListadoUsuarios(SingleTableView):
	model = Usuario
	template_name = 'usuarios/listado.html'
	table_class = UsuarioTable
	table_data = Usuario.usuarios.all()
	paginate_by = 12

class NuevoUsuario(GenericAltaView):
	model = Usuario
	form_class = UsuarioForm
	template_name = 'usuarios/alta.html'
	success_url = reverse_lazy('usuarios:listado')
	cargar_otro_url = reverse_lazy('usuarios:alta')

class ModificarUsuario(UpdateView):
	model = Usuario
	form_class = UsuarioForm
	success_url = reverse_lazy('usuarios:listado')
	template_name = 'usuarios/alta.html'

class EliminarUsuario(GenericEliminarView):
	model = Usuario
	success_url = reverse_lazy('usuarios:listado')
	