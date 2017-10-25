from django import forms
from .models import Modulo

class ModuloForm(forms.ModelForm):
	class Meta:
		model = Modulo

		fields = [
				'codigo'
				'nombre',
				'descripcion',
			]
		labels = {
				'codigo': 'Codigo'
				'nombre': 'Nombre',
				'descripcion': 'Descripcion',
		}

		widgets = {
			'codigo':forms.TextInput(attrs={'class':'form-control'}),
			'nombre':forms.TextInput(attrs={'class':'form-control'}),
			'descripcion':forms.Textarea(attrs={'class':'form-control'}),
		}