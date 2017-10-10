from django import forms
from .models import Localidad

class LocalidadForm(forms.ModelForm):
	class Meta:
		model = Localidad

		fields = [
				'codpostal',
				'nombre',
				'departamento',
			]
		labels = {
				'codpostal': 'Codigo Postal',
				'nombre': 'Nombre',
				'departamento': 'Departamento',
		}

		widgets = {
			'codpostal':forms.TextInput(attrs={'class':'form-control'}),
			'nombre':forms.TextInput(attrs={'class':'form-control'}),
			'departamento':forms.Select(attrs={'class':'form-control'}),
		}