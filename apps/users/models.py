from django.db import models
from django.contrib.auth.models import AbstractUser
from ..personas.models import Persona

class Usuario(AbstractUser):
	persona = models.ForeignKey("personas.Persona", on_delete=models.CASCADE)

