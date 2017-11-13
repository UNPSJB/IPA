from django import forms
from .models import Establecimiento
from .models import Afluente
from .models import Departamento
from .models import Localidad

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
			'duenio':forms.Select(attrs={'class':'form-control'}),
			'codigoCatastral':forms.TextInput(attrs={'class':'form-control'}),
			'superficie':forms.TextInput(attrs={'class':'form-control'}),
			'nombre':forms.TextInput(attrs={'class':'form-control'}),
			'descripcion':forms.Textarea(attrs={'class':'form-control'}),
			'localidad':forms.Select(attrs={'class':'form-control'}),
		}

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