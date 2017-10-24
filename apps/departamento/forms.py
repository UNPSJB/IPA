from django import forms
from .models import Departamento

class DepartamentoForm(forms.ModelForm):
	class Meta:
		model = Departamento

		fields = [
				'nombre',
				'superficie',
				'poblacion',
				'descripcion',
			]
		labels = {
				'nombre': 'Nombre',
				'superficie': 'Superficie',
				'poblacion': 'Poblacion',
				'descripcion': 'Descripcion',
		}

		widgets = {
			'nombre':forms.TextInput(attrs={'class':'form-control'}),
			'superficie':forms.TextInput(attrs={'class':'form-control'}),
			'poblacion':forms.TextInput(attrs={'class':'form-control'}),
			'descripcion':forms.Textarea(attrs={'class':'form-control'}),
		}

