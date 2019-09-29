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

		# TODO: Validaciones de numero documento y telefono.

		widgets = {
			'nombre':forms.TextInput(attrs={'class':'form-control', 'placehorder':'Nombre'}),
			'apellido':forms.TextInput(attrs={'class':'form-control', 'placehorder':'Apellido'}),
			'email':forms.TextInput(attrs={'class':'form-control', 'placehorder':'Email'}),
			'tipoDocumento':forms.Select(attrs={'class':'form-control', 'placehorder':'Seleccione el tipo de documento'}),
			'numeroDocumento':forms.TextInput(attrs={'class':'form-control', 'placehorder':'Numero de documento'}),
			'direccion':forms.TextInput(attrs={'class':'form-control', 'placehorder':'Domicilio del solicitante'}),
			'telefono':forms.TextInput(attrs={'class':'form-control','type':'number', 'placehorder':'Telefono con o sin catacteristica'}),
		}

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

class ChoferForm (forms.ModelForm):
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
		
