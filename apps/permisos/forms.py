from django import forms
from .models import Permiso, TipoUso, Estado, Solicitado

class PermisoForm(forms.ModelForm):
	class Meta:
		model = Permiso

		fields = [
			'solicitante',
			'establecimiento',
			'tipo',
			'afluente',
			]
		labels = {
			'solicitante' : 'Solicitante',
			'establecimiento' : 'Establecimiento',
			'tipo' : 'Tipo',
			'afluente' : 'Afluente',
			}

		widgets = {
			'solicitante':forms.Select(attrs={'class':'form-control'}),
			'establecimiento':forms.Select(attrs={'class':'form-control'}),
			'tipo':forms.Select(attrs={'class':'form-control'}),
			'afluente':forms.Select(attrs={'class':'form-control'}),
			}


class TipoDeUsoForm(forms.ModelForm):
	class Meta:
		model = TipoUso

		fields = [
				'descripcion',
				'coeficiente',
				'periodo',
				'medida',
				'tipo_modulo',
				'documentos',
			]
		labels = {
				'descripcion': 'Descripcion',
				'coeficiente': 'Coeficiente',
				'periodo': 'Periodo',
				'medida': 'Medida',
				'tipo_modulo': 'Tipo de módulo',
				'documentos': 'Documentos requeridos',
		}

		widgets = {
			'descripcion':forms.TextInput(attrs={'class':'form-control'}),
			'coeficiente':forms.TextInput(attrs={'class':'form-control'}),
			'periodo':forms.Select(attrs={'class':'form-control'}),
			'medida':forms.Select(attrs={'class':'form-control'}),
			'tipo_modulo':forms.Select(attrs={'class':'form-control'}),
			'documentos':forms.SelectMultiple(attrs={'class':'form-control'}),
		}

class SolicitadoForm(forms.ModelForm):
	class Meta:
		model = Solicitado

		fields = [
			'fecha',
			'observacion',
			'utilizando',
			'oficio'
		]
		labels = {
			'fecha': 'Fecha',
			'observacion': 'Observación', 
			'utilizando': 'Utilizando',
		}

		widgets = {
			'utilizando':forms.CheckboxInput(attrs={'class':'form-control'}),
			'fecha': forms.DateInput(attrs={'type':'date'}),
			'observacion': forms.Textarea(attrs={'class':'form-control'}), 
	}
