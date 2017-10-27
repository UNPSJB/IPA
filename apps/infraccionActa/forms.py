from django import forms
from .models import InfraccionActa

class InfraccionActaForm(forms.ModelForm):
	class Meta:
		model = InfraccionActa

		fields = [
				'numero',
				'fecha',
				'oficialSumariante',
				#'estado',
				'fechaArchivado',
				#'tipoDocumento', ESCANEADO
				'establecimiento',
				'descripcion',
			]
		labels = {
				'numero': 'Numero',
				'fecha': 'Fecha de infraccion',
				'oficialSumariante': 'Oficial Sumariante',
				#'estado': 'Estado',
				'fechaArchivado': 'Fecha de archivado',
				#'tipoDocumento': 'Tipo de Documento', ESCANEADO
				'establecimiento': 'Establecimiento',
				'descripcion': 'Descripcion',
		}

		widgets = {
			'numero':forms.TextInput(attrs={'class':'form-control'}),
			'fecha':forms.TextInput(attrs={'class':'form-control'}),
			'oficialSumariante':forms.Select(attrs={'class':'form-control'}),
			#'estado':forms.Textarea(attrs={'class':'form-control'}),
			'fechaArchivado':forms.TextInput(attrs={'class':'form-control'}),
			#'tipoDocumento':forms.Select(attrs={'class':'form-control'}), ESCANEADO
			'establecimiento':forms.Select(attrs={'class':'form-control'}),
			'descripcion':forms.Textarea(attrs={'class':'form-control'}),
		}

