from django import forms
from .models import Permiso, TipoUso, Solicitado
from ..personas.models import Persona
from datetime import date
from datetime import datetime
from django.core.exceptions import ValidationError

class PermisoForm(forms.ModelForm):
	class Meta:
		model = Permiso

		fields = [
			'solicitante',
			'establecimiento',
			'tipo',
			'afluente',
			]
		labels = {
			'solicitante' : 'Solicitante',
			'establecimiento' : 'Establecimiento',
			'tipo' : 'Tipo de uso de agua',
			'afluente' : 'Afluente',
			}

		widgets = {
			'solicitante':forms.Select(attrs={'class':'form-control', 'placeholder':'Solicitante'}),
			'establecimiento':forms.Select(attrs={'class':'form-control', 'placeholder':'Establecimiento'}),
			'tipo':forms.Select(attrs={'class':'form-control', 'placeholder':'Tipo de Uso'}),
			'afluente':forms.Select(attrs={'class':'form-control', 'placeholder':'Afluente de donde toma el recurso hidrico'}),
			}

	def __init__(self, *args, **kwargs):
		super(PermisoForm, self).__init__(*args,**kwargs)
		self.fields['solicitante'].queryset = Persona.objects.all().filter(roles__tipo=5)

class TipoDeUsoForm(forms.ModelForm):
	class Meta:
		model = TipoUso

		fields = [
				'descripcion',
				'coeficiente',
				'periodo',
				'medida',
				'tipo_modulo',
				'documentos',
			]
		labels = {
				'descripcion': 'Nombre',
				'coeficiente': 'Coeficiente',
				'periodo': 'Periodo',
				'medida': 'Medida',
				'tipo_modulo': 'Tipo de módulo',
				'documentos': 'Documentos requeridos',
		}

		widgets = {
			'descripcion':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre' }),
			'coeficiente':forms.TextInput(attrs={'class':'form-control', 'type':'number', 'step':'0.01', 'min':'0.01', 'placeholder':'Coeficiente'}),
			'periodo':forms.Select(attrs={'class':'form-control', 'placeholder':'Periodo'}),
			'medida':forms.Select(attrs={'class':'form-control', 'placeholder':'Medida'}),
			'tipo_modulo':forms.Select(attrs={'class':'form-control', 'placeholder':'Tipo de Módulo'}),
			'documentos':forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Documentos'}),
		}

class SolicitadoForm(forms.ModelForm):
	class Meta:
		model = Solicitado

		fields = [
			'fecha',
			'observacion',
			'utilizando',
			'oficio'
		]
		labels = {
			'fecha': 'Fecha',
			'observacion': 'Observación', 
			'utilizando': 'Utilizando',
		}

		widgets = {
			'utilizando':forms.CheckboxInput(attrs={'class':'form-control'}),
			'fecha': forms.DateInput(format=('%Y-%m-%d'),attrs={'type':'date'}),
			'observacion': forms.Textarea(attrs={'class':'form-control'}), 
	}

	def clean_fecha(self):
		fecha_form = self.cleaned_data.get('fecha')

		if (fecha_form>date.today()):
			raise ValidationError("La fecha de solicitud no puede ser mayor a la fecha actual ("+date.today().strftime("%d-%m-%Y")+")")
		
		return fecha_form