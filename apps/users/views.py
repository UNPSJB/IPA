from django.shortcuts import render
from .models import Usuario
from .tables import UsuarioTable
from django_tables2 import SingleTableView
from apps.generales.views import GenericAltaView
# Create your views here.

class ListadoUsuarios(SingleTableView):
	model = Usuario
	template_name = 'usuarios/listado.html'
	table_class = UsuarioTable
	paginate_by = 12

# class NuevoUsuario(GenericAltaView):
# 	model = Usuario
# 	form_class = UsuarioForm
# 	template_name = 'usuario/alta.html'
# 	success_url = reverse_lazy('usuarios:listado')
# 	cargar_otro_url = reverse_lazy('usuario:alta')

# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		return context