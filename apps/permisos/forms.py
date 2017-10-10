from django import forms
from .models import Permiso, Solicitud

class PermisoForm(forms.ModelForm):
	class Meta:
		model = Permiso

		fields = [
			]
		labels = {
		}

		widgets = {
		}


class SolicitudForm(forms.ModelForm):
	class Meta:
		model = Solicitud

		fields = [
			'fecha_solicitud',
			'solicitante',
			'establecimiento',
			'tipo',
			'afluente',
			'utilizando',
			]
		labels = {
			'fecha_solicitud' : 'Fecha',
			'solicitante' : 'Solicitante',
			'establecimiento' : 'Establecimiento',
			'tipo' : 'Tipo',
			'afluente' : 'Afluente',
			'utilizando' : 'Utilizando',
			}

		widgets = {
	#		'fecha_solicitud' : forms.DateField(widget=forms.DateInput()),
	#		'solicitante' : forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple),
	#		'establecimiento' : forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple),
	#		'tipo' : forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple),
	#		'afluente' : forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple),
	#		'utilizando' : forms.MultipleChoiceField(widget=forms.CheckboxInput()),
			}