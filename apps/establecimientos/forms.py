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
			'duenio':forms.Select(attrs={'class':'form-control', 'placeholder':'Dueño del establecimiento'}),
			'codigoCatastral':forms.TextInput(attrs={'class':'form-control','type':'number', 'min':'1', 'placeholder':'Codigo Catastral'}),
			'superficie':forms.TextInput(attrs={'class':'form-control','type':'number', 'step':'0.01', 'min':'1', 'placeholder':'Superficie'}),
			'nombre':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del establecimiento'}),
			'descripcion':forms.Textarea(attrs={'class':'form-control'}),
			'localidad':forms.Select(attrs={'class':'form-control', 'placeholder':'Localidad'}),
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
			'nombre':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}),
			'localidad':forms.Select(attrs={'class':'form-control', 'placeholder':'Localidad'}),
			'caudal':forms.TextInput(attrs={'class':'form-control', 'type':'number', 'step':'0.01', 'min':'1', 'placeholder':'Caudal (en metros cubicos)'}),
			'longitud':forms.TextInput(attrs={'class':'form-control', 'type':'number','step':'0.01', 'min':'1', 'placeholder':'Longitud (en metros cuadrados)'}),
			'superficie':forms.TextInput(attrs={'class':'form-control', 'type':'number', 'step':'0.01', 'min':'1', 'placeholder':'Superficie'}),
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
			'nombre':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}),
			'superficie':forms.TextInput(attrs={'class':'form-control','type':'number', 'min':'1', 'placeholder':'Superficie (en metros cuadrados)'}),
			'poblacion':forms.TextInput(attrs={'class':'form-control', 'type':'number', 'min':'1', 'placeholder':'Cantidad de habitantes'}),
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
			'codpostal':forms.TextInput(attrs={'class':'form-control', 'type':'number', 'min':'1', 'placeholder':'Codigo Postal'}),
			'nombre':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}),
			'departamento':forms.Select(attrs={'class':'form-control', 'placeholder':'Departamento'}),
		}