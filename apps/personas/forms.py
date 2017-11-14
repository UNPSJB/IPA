from django import forms
from .models import *

from django.core.exceptions import ObjectDoesNotExist


class PersonaForm(forms.ModelForm):
	class Meta:
		model = Persona

		fields = [
				'nombre',
				'apellido',
				'email',
				'tipoDocumento',
				'numeroDocumento',
				'razonSocial',
				'direccion',
				'telefono',
			]
		labels = {
				'nombre': 'Nombre',
				'apellido': 'Apellido',
				'email': 'Email',
				'tipoDocumento': 'Tipo Documento',
				'numeroDocumento': 'Nro. Documento',
				'razonSocial': 'Razon Social',
				'direccion': 'Dirección',
				'telefono': 'Teléfono',
		}

		widgets = {
			'nombre':forms.TextInput(attrs={'class':'form-control'}),
			'apellido':forms.TextInput(attrs={'class':'form-control'}),
			'email':forms.TextInput(attrs={'class':'form-control'}),
			'tipoDocumento':forms.Select(attrs={'class':'form-control'}),
			'numeroDocumento':forms.TextInput(attrs={'class':'form-control'}),
			'razonSocial':forms.TextInput(attrs={'class':'form-control'}),
			'direccion':forms.TextInput(attrs={'class':'form-control'}),
			'telefono':forms.TextInput(attrs={'class':'form-control'}),
		}
		

class DetallePersonaForm(forms.Form):
	pass


class DirectorForm (forms.ModelForm):
	class Meta:
		model=Director
		fields = [
			'legajo',
			'cargo',
			'fechaInicio',
		]

		#fields = '__all__'
		#exclude = ['nombre','apellido']
		
	#def save(self):
		#personaForm = PersonaForm(data=self.cleaned_data)
	#	try:
			#persona = personaForm.save()
	#		director = super().save()
	#		persona.agregar_rol(director)
	#		return director
	#	except ValueError:
	#		return None

class AdministrativoForm (forms.Form):
	pass
	#class Meta:
	#	model=Administrativo

class InspectorForm (PersonaForm):
	pass

class OficialSumarianteForm (InspectorForm):
	pass

class JefeDepartamentoForm (PersonaForm):
	pass

class ChoferForm (PersonaForm):
	pass

class SolicitanteForm (PersonaForm):
	pass

class LiquidadorForm (PersonaForm):
	pass

#AdministrativoForm.base_fields.update(PersonaForm.base_fields)




