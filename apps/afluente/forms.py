from django import forms
from .models import Afluente

class AfluenteForm(forms.ModelForm):
	class Meta:
		model = Afluente

		fields = [
				'nombre',
				'localidad',
				'caudal',
				'longitud',
				'superficie',
				'descripcion',
			]
		labels = {
				'nombre': 'Nombre',
				'localidad': 'Localidad',
				'caudal': 'Caudal',
				'longitud': 'Longitud',
				'superficie': 'Superficie',
				'descripcion': 'Descripcion',
		}

		widgets = {
			'nombre':forms.TextInput(attrs={'class':'form-control'}),
			'localidad':forms.Select(attrs={'class':'form-control'}),
			'caudal':forms.TextInput(attrs={'class':'form-control'}),
			'longitud':forms.TextInput(attrs={'class':'form-control'}),
			'superficie':forms.TextInput(attrs={'class':'form-control'}),
			'descripcion':forms.Textarea(attrs={'class':'form-control'}),
		}