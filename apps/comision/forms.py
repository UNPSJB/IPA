from django import forms
from .models import Comision

class ComisionForm(forms.ModelForm):
	class Meta:
		model = Comision

		fields = [
				'empleado',
				'reclamos',
				'departamento',
				'localidad',
				'fechaInicio',
				'fechaFin',
			]
		labels = {
				'empleado':'Empleado',
				'reclamos':'Reclamos',
				'departamento':'Departamento',
				'localidad':'Localidad',
				'fechaInicio':'Fecha de inicio',
				'fechaFin':'Fecha de finalizacion',
		}

		widgets = {
			'empleado':forms.Select(attrs={'class':'form-control'}),
			'reclamos':forms.Select(attrs={'class':'form-control'}),
			'departamento':forms.Select(attrs={'class':'form-control'}),
			'localidad':forms.Select(attrs={'class':'form-control'}),
			'fechaInicio':forms.TextInput(attrs={'class':'form-control'}),
			'fechaFin':forms.TextInput(attrs={'class':'form-control'}),
		}