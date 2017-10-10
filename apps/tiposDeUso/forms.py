from django import forms
from .models import TipoUso

class AltaForm(forms.ModelForm):
	class Meta:
		model = TipoUso

		fields = [
				'nombre',
				'coeficiente',
				'periodo',
				'medida',
				'documentos',
			]
		labels = {
				'nombre': 'Nombre',
				'coeficiente': 'Coeficiente',
				'periodo': 'Periodo',
				'medida': 'Medida',
				'documentos': 'Documentos',
		}

		widgets = {
			'nombre':forms.TextInput(attrs={'class':'form-control'}),
			'coeficiente':forms.TextInput(attrs={'class':'form-control'}),
			'periodo':forms.TextInput(attrs={'class':'form-control'}),
			'medida':forms.TextInput(attrs={'class':'form-control'}),
			'documentos':forms.TextInput(attrs={'class':'form-control'}),
		}