from django import forms
from .models import ValorDeModulo, Cobro

class RegistrarValorDeModuloForm(forms.ModelForm):
	class Meta:
		model = ValorDeModulo

		fields = [
				'modulo',
				'precio',
				'fecha',
				'descripcion',
			]
		labels = {
				'modulo': 'Modulo',
				'precio':'Precio',
				'fecha':'Fecha',
				'descripcion':'Descripcion',
		}

		widgets = {
				'modulo': forms.TextInput(attrs={'class':'form-control'}),
				'precio':forms.TextInput(attrs={'class':'form-control'}),
				'descripcion':forms.TextInput(attrs={'class':'form-control'}),
				'fecha':forms.DateInput(attrs={'class':'form-control'}),
		}

class CobroForm(forms.ModelForm):
	class Meta:
		model = Cobro

		fields = [
				'monto',
				'documento',
				'fecha',
		]

		labels = {
				'monto': 'Monto',
				'documento':'Documento',
				'fecha':'Fecha',
		}