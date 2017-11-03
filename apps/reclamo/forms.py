from django import forms
from .models import Reclamo

class ReclamoForm(forms.ModelForm):
	class Meta:
		model = Reclamo
		
		fields = [
				'persona',
				'lugar',
				'fecha',
				'motivo',
			]
		labels = {
				'persona': 'Persona',
				'lugar': 'Lugar',
				'fecha': 'Fecha',
				'motivo': 'Motivo',

		}

		widgets = {
			'persona':forms.TextInput(attrs={'class':'form-control'}),
			'lugar':forms.TextInput(attrs={'class':'form-control'}),
			'fecha':forms.TextInput(attrs={'class':'form-control'}),
			'motivo':forms.TextInput(attrs={'class':'form-control'}),

		}