from django.db import models

# Create your models here.
class Persona(models.Model):
	nombre = models.CharField(max_length=30)
	apellido = models.CharField(max_length=30)
	email = models.EmailField()
	tipoDocumento = models.CharField(max_length=10)
	numeroDocumento = models.CharField(max_length=15)
	razónSocial = models.CharField(max_length=10)
	dirección = models.CharField(max_length=60)
	teléfono = models.IntegerField()

	def __str__(self):
		return "{}, {}".format(self.apellido, self.nombre)

class Rol(models.Model):
	rolname = models.CharField(max_length=20)
    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        null=True
    )

class Director(Rol):
	
	def __init__(self):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.rolname = "Director"
        self.legajo = models.IntegerField()
		self.cargo = models.CharField(max_length=25)
		#fecha inicio de cargo
		self.fechaInicio = models.DateField()

class Administrativo(Rol):

	def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.rolname = "Administrativo"

class Inspector(Rol):

	def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.rolname = "Inspector"

class JefeDepartamento(Rol):

	def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.rolname = "Jefe de departamento"

class Chofer(Rol):

	def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.rolname = "Jefe de departamento"
        self.licencia = models.CharField(max_length=20)
        self.vencimientoLicencia = models.DateField()
        #tipo ?????????????????

class Solicitante(Rol):

	def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.rolname = "Solicitante"
