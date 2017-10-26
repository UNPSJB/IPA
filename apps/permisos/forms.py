from django import forms
from .models import Permiso, Solicitud

class PermisoForm(forms.ModelForm):
	class Meta:
		model = Permiso

		fields = [
			]
		labels = {
		}

		widgets = {
		}


class SolicitudForm(forms.ModelForm):
	class Meta:
		model = Solicitud

		fields = [
			'fecha_solicitud',
			'solicitante',
			'establecimiento',
			'tipo',
			'afluente',
			'utilizando',
			]
		labels = {
			'fecha_solicitud' : 'Fecha',
			'solicitante' : 'Solicitante',
			'establecimiento' : 'Establecimiento',
			'tipo' : 'Tipo',
			'afluente' : 'Afluente',
			'utilizando' : 'Utilizando',
			}

		widgets = {
			'fecha_solicitud':forms.TextInput(attrs={'class':'form-control'}),
			'solicitante':forms.Select(attrs={'class':'form-control'}),
			'establecimiento':forms.Select(attrs={'class':'form-control'}),
			'tipo':forms.Select(attrs={'class':'form-control'}),
			'afluente':forms.Select(attrs={'class':'form-control'}),
		#	'utilizando':forms.BooleanField(required=False),
			}