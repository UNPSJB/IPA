from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.persona.models import Rol

class Usuario(Rol, AbstractUser):
        