from django import forms
from .models import TipoDocumentacion

class TipoDocumentacionForm(forms.ModelForm):
	class Meta:
		model = TipoDocumentacion

		fields = [
				'nombre',
			]
		labels = {
				'nombre': 'Nombre',
	
		}

		widgets = {
			'nombre':forms.TextInput(attrs={'class':'form-control'}),
		
		}
