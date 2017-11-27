from django import forms
from .models import ValorDeModulo, Pago

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
				'fecha': forms.DateInput(attrs={'type':'date'}),
		}

class PagoForm(forms.ModelForm):
	class Meta:
		model = Pago

		fields = [
				'monto',
				'fecha',
			]
		labels = {
				'monto':'Monto ($)',
				'fecha':'Fecha de Pago',
		}

		widgets = {
				'monto':forms.TextInput(attrs={'class':'form-control'}),
				'fecha': forms.DateInput(attrs={'type':'date'}),
		}