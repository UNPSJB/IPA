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
				'direccion',
				'telefono',
			]
		labels = {
				'nombre': 'Nombre',
				'apellido': 'Apellido',
				'email': 'Email',
				'tipoDocumento': 'Tipo Documento',
				'numeroDocumento': 'Nro. Documento',
				'direccion': 'Dirección',
				'telefono': 'Teléfono',
		}

		widgets = {
			'nombre':forms.TextInput(attrs={'class':'form-control', 'placehorder':'Nombre'}),
			'apellido':forms.TextInput(attrs={'class':'form-control', 'placehorder':'Apellido'}),
			'email':forms.TextInput(attrs={'class':'form-control', 'placehorder':'email@email.com'}),
			'tipoDocumento':forms.Select(attrs={'class':'form-control', 'placehorder':'Seleccione el tipo de documento'}),
			'numeroDocumento':forms.TextInput(attrs={'class':'form-control','type':'number', 'min':'1000000', 'placehorder':'Numero de documento sin .'}),
			'direccion':forms.TextInput(attrs={'class':'form-control', 'placehorder':'Domicilio del solicitante'}),
			'telefono':forms.TextInput(attrs={'class':'form-control','type':'number', 'min':'150000000', 'placehorder':'Telefono con o sin catacteristica'}),
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
		ordering = ["-legajo"]

		widgets = {

			'fechaInicio': forms.DateInput(attrs={'type':'date'}),
		}
		
	#def save(self):
		#personaForm = PersonaForm(data=self.cleaned_data)
	#	try:
			#persona = personaForm.save()
	#		director = super().save()
	#		persona.agregar_rol(director)
	#		return director
	#	except ValueError:
	#		return None

class AdministrativoForm (PersonaForm):
	
	class Meta:
		model = Administrativo
		fields = [
			'tipo',
		]

		exclude = [
			'tipo'
		]

class InspectorForm (PersonaForm):
	pass

class OficialSumarianteForm (InspectorForm):
	pass

class JefeDepartamentoForm (PersonaForm):
	pass

class ChoferForm (PersonaForm):
	class Meta:
		model=Chofer
		fields = [
			'licencia',
			'vencimientoLicencia',
		]
		ordering = ["-vencimientoLicencia"]

		labels = {
				'licencia': 'Licencia',
				'vencimientoLicencia': 'Vencimiento de la Licencia',
		}

		widgets = {
			'licencia':forms.TextInput(attrs={'class':'form-control'}),
			'vencimientoLicencia': forms.DateInput(attrs={'type':'date'}),
		}

class SolicitanteForm (PersonaForm):
	pass

class LiquidadorForm (PersonaForm):
	pass

#AdministrativoForm.base_fields.update(PersonaForm.base_fields)
AdministrativoForm.base_fields.update()

class EmpresaForm(forms.ModelForm):
	class Meta:
		model = Empresa
		fields = [
				'cuit',
				'razonSocial',
				'direccion',
				'telefono'
			]
		labels = {
				'cuit': 'CUIT',
				'razonSocial': 'Razón Social',
				'direccion': 'Dirección',
				'telefono': 'Teléfono'
		}
		widgets = {
			'cuit':forms.TextInput(attrs={'class':'form-control','type':'number', 'min':'10000000000', 'placehorder':'Número de CUIT'}),
			'razonSocial':forms.TextInput(attrs={'class':'form-control', 'placehorder':'Razón Social'}),
			'direccion':forms.TextInput(attrs={'class':'form-control', 'placehorder':'Domicilio del solicitante'}),
			'telefono':forms.TextInput(attrs={'class':'form-control','type':'number', 'min':'150000000', 'placehorder':'Telefono con o sin catacteristica'}),
		}
		
