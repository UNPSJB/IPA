from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from ..personas.models import Persona

class UsuariosManager(UserManager):
	
	def __init__(self, show_superusers=False):
		super().__init__()
		self.show_superusers = show_superusers


	def get_queryset(self):
		qs = super().get_queryset()
		if not self.show_superusers:
			qs = qs.filter(is_superuser=False)
		return qs

class Usuario(AbstractUser):
	persona = models.ForeignKey("personas.Persona", on_delete=models.CASCADE, null=True)
	objects =  UsuariosManager(show_superusers=True)
	usuarios = UsuariosManager()

	class Meta:
		permissions = (
			("listar_usuarios","Listar usuarios"),
			("cargar_empresa","Cargar empresas"),
			("detalle_empresa","Ver detalle de empresas"),
			("modificar_empresa","Modificar empresas"),
			("eliminar_empresa","Eliminar empresas")
		)