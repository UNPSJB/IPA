from django import forms
from .models import Establecimiento

class EstablecimientoForm(forms.ModelForm):
	class Meta:
		model = Establecimiento

		fields = [
				'duenio',
				'codigoCatastral',
				'superficie',
				'nombre',
				'descripcion',
				'localidad',
			]

		labels = {
				'duenio': 'Dueño',
				'codigoCatastral': 'Cod. Catastral',
				'superficie': 'Superficie',
				'nombre': 'Nombre',
				'descripcion': 'Descripción',
				'localidad': 'Localidad',
		}

		widgets = {
			'duenio':forms.TextInput(attrs={'class':'form-control'}),
			'codigoCatastral':forms.TextInput(attrs={'class':'form-control'}),
			'superficie':forms.TextInput(attrs={'class':'form-control'}),
			'nombre':forms.TextInput(attrs={'class':'form-control'}),
			'descripcion':forms.Textarea(attrs={'class':'form-control'}),
			'localidad':forms.Select(attrs={'class':'form-control'}),
		}