from django.db import models
from django.contrib.auth.models import AbstractUser
from ..personas.models import Persona

class UsuariosManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(is_superuser=False)


class Usuario(AbstractUser):
	persona = models.ForeignKey("personas.Persona", on_delete=models.CASCADE, null=True)

	objects = UsuariosManager()