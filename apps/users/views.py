from django.shortcuts import render
from .models import Usuario
from .tables import UsuarioTable
from django_tables2 import SingleTableView

# Create your views here.

class ListadoUsuarios(SingleTableView):
	model = Usuario
	template_name = 'usuarios/listado.html'
	table_class = UsuarioTable
	paginate_by = 12
