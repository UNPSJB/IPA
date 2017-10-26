from django import forms
from .models import Expediente

class ExpedienteForm(forms.ModelForm):
	class Meta:
		model = Expediente

		fields = [
				'fecha',
				'numero',
				'extracto',
				]
		labels = {
				'fecha': 'Fecha',
				'numero': 'Numero',
				'extracto': 'Extracto',
		}

		widgets = {
			'fecha':forms.TextInput(attrs={'class':'form-control'}),
			'numero':forms.TextInput(attrs={'class':'form-control'}),
			'extracto':forms.TextInput(attrs={'class':'form-control'}),
		}