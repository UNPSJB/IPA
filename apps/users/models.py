from django.db import models
from django.contrib.auth.models import AbstractUser
from ..personas.models import Rol

class Usuario(AbstractUser, Rol):

	TIPO = 8
	def __init__(self, *args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)

