from django import forms
from .models import Comision

class ComisionForm(forms.ModelForm):
	class Meta:
		model = Comision

		fields = [
				'empleados',
				'localidades',
				'fechaInicio',
				'fechaFin',
			]
		labels = {
				'empleados':'Empleados',
				'localidades':'Localidades',
				'fechaInicio':'Fecha de inicio',
				'fechaFin':'Fecha de finalizacion',
		}

		widgets = {
			'empleados':forms.SelectMultiple(attrs={'class':'form-control'}),
			'localidades':forms.SelectMultiple(attrs={'class':'form-control'}),
			'fechaInicio':forms.DateInput(attrs={'type':'date'}),
			'fechaFin':forms.DateInput(attrs={'type':'date'}),
		}