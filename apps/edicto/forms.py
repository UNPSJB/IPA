from django import forms
from .models import Edicto

class EdictoForm(forms.ModelForm):
	class Meta:
		model = Edicto

		fields = [
				'numero',
				'fechaPublicacion',
				'fechaExigencia',
				#'expediente',
			]
		labels = {
				'numero': 'Numero',
				'fechaPublicacion': 'Fecha de publicaicon',
				'fechaExigencia': 'Fecha de exigencia',
		}

		widgets = {
			'numero':forms.TextInput(attrs={'class':'form-control'}),
			'fechaPublicacion':forms.TextInput(attrs={'class':'form-control'}),
			'fechaExigencia':forms.TextInput(attrs={'class':'form-control'}),
		}