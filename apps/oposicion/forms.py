from django import forms
from .models import Oposicion

class OposicionForm(forms.ModelForm):
	class Meta:
		model = Oposicion

		fields = [
				'numero',
				'persona',
				'fecha',
				'descripcion',
				'documento',
			]
		labels = {
				'numero': 'Numero',
				'persona': 'Persona',
				'fecha': 'Fecha',
				'descripcion': 'Descripcion',
				'documento': 'Documento',
		}

		widgets = {
			'numero':forms.TextInput(attrs={'class':'form-control'}),
			'persona':forms.Select(attrs={'class':'form-control'}),
			'fecha':forms.TextInput(attrs={'class':'form-control'}),
			'descripcion':forms.Textarea(attrs={'class':'form-control'}),
			'documento':forms.TextInput(attrs={'class':'form-control'}),
			
		}