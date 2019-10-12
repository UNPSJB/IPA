from django import forms
from .models import *
from apps.personas.models import Persona


class CustomModelChoiceField(forms.ModelChoiceField):
	to_field_name = 'id'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def label_from_instance(self, obj):
		return "{} {}".format(obj.nombre, obj.apellido)
	
class UsuarioForm(forms.ModelForm):
	class Meta:
		model = Usuario
		fields = [
				'username',
				'password',
				'email',
				'persona'
			]
		labels = {
				'username': 'Nombre de Usuario',
				'password': 'Contraseña',
				'email': 'Email',
				'persona': 'Persona'
		}

		widgets = {
			'username':forms.TextInput(attrs={'class':'form-control', 'placehorder':'Nombre'}),
			'password':forms.TextInput(attrs={'class':'form-control', 'placehorder':'Apellido'}),
			'email':forms.TextInput(attrs={'class':'form-control', 'placehorder':'Email'}),
			'persona': forms.Select(attrs={'class':'form-control', 'placeholder':'Persona'})
		}
