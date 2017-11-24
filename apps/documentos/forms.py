from django import forms
from .models import TipoDocumento, Documento

class TipoDocumentoForm(forms.ModelForm):
	class Meta:
		model = TipoDocumento

		fields = [
				'nombre',
			]
		labels = {
				'nombre': 'Nombre',
	
		}

		widgets = {
			'nombre':forms.TextInput(attrs={'class':'form-control'}),
	
		}

class DocumentoForm(forms.ModelForm):
	class Meta:
		model = Documento

		fields = [
				'tipo',
				'descripcion',
				'archivo',
				'fecha',
			]
		labels = {
				'tipo':'Tipo',
				'descripcion':'Descripcion',
				'archivo':'Archivo',
				'fecha':'Fecha del Tipo de Documento',
		}

		widgets = {
				'tipo':forms.Select(attrs={'class':'form-control'}),
				'descripcion':forms.TextInput(attrs={'class':'form-control'}),
				'fecha':forms.DateInput(attrs={'class':'form-control'}),
		}