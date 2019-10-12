from django import forms
from .models import *
from apps.personas.models import Persona
	
# TODO mejorar este form para  usuarios.

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
			'password':forms.TextInput(attrs={'class':'form-control', 'placehorder':'Apellido', 'type':'password'}),
			'email':forms.TextInput(attrs={'class':'form-control', 'placehorder':'Email'}),
			'persona': forms.Select(attrs={'class':'form-control', 'placeholder':'Persona'})
		}
