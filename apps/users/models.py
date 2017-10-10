from django.db import models
from django.contrib.auth.models import AbstractUser
from ..personas.models import Rol

class Usuario(AbstractUser, Rol):
	pass
