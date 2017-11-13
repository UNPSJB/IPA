from django import forms
from .models import TipoDocumento

class TipoDocumentoForm(forms.ModelForm):
	class Meta:
		model = TipoDocumento

		fields = [
				'nombre',
			]
		labels = {
				'nombre': 'Nombre',
	
		}

		widgets = {
			'nombre':forms.TextInput(attrs={'class':'form-control'}),
	
		}

