from django import forms
from .models import *
from apps.personas.models import Persona

# TODO mejorar este form para  usuarios.

class UsuarioForm(forms.Form):
	username = forms.CharField(label='Nombre de usuario' ,required=True)
	password = forms.CharField(label='Contraseña', required=True)
	confirmar_password = forms.CharField(label='Repita la contraseña', required=True) 
	email = forms.EmailField(label='Email', required=True)
	persona = forms.ModelChoiceField(required=True, queryset=Persona.objects.filter(usuario__isnull=True), label="Persona")
		
	def clean(self):
		cleaned_data = super(UsuarioForm, self).clean()
		password = cleaned_data.get('password')
		confirmar_password = cleaned_data.get('confirmar_password')

		if password and confirmar_password and password != confirmar_password:
			self._errors['confirmar_password'] = self.error_class(['Los passwords no son iguales.'])
			del self.cleaned_data['confirmar_password']
		return cleaned_data

	def save(self):
		cleaned_data = self.clean()
		username = cleaned_data.get('username')
		password = cleaned_data.get('password')
		email = cleaned_data.get('email')

		usuario = Usuario.objects.create_user(username=username,password=password, email=email)
		persona = cleaned_data.get('persona')
		usuario.persona = persona
		usuario.save()