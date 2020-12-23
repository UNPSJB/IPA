from django import forms
from .models import Comision
from ..personas.models import Persona

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
			'empleados':forms.SelectMultiple(attrs={'class':'form-control','id':'empleados'}),
			'localidades':forms.SelectMultiple(attrs={'class':'form-control','id':'localidades'}),
			'fechaInicio':forms.DateInput(attrs={'type':'date','id':'fechaInicio'}),
			'fechaFin':forms.DateInput(attrs={'type':'date','id':'fechaFin'}),
		}

	def __init__(self, *args, **kwargs):
		super(ComisionForm, self).__init__(*args,**kwargs)
		self.fields['empleados'].queryset = Persona.getEmpleadosParaComision()		