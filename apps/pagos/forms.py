from django import forms
from .models import ValorDeModulo, Cobro, Pago
from datetime import date, datetime

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
				'modulo': forms.Select(attrs={'class':'form-control', 'placeholder':'Elija un modulo'}),
				'precio':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Precio'}),
				'descripcion':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Descripcion'}),
				'fecha': forms.DateInput(attrs={'type':'date'}),
		}

class CobroForm(forms.Form):
	descripcion = forms.CharField(label='Concepto del Cobro')
	archivo = forms.FileField(label='Adjuntar el Documento del Cobro')
	fecha_desde = forms.DateField(disabled=True,label="Fecha desde",widget=forms.DateInput(format=('%Y-%m-%d'),attrs={'class':'form-control','type':'date','data-tooltip':"Fecha desde el ultimo cobro"}))
	fecha_hasta = forms.DateField(initial=date.today(),label="Fecha hasta",
					widget=forms.DateInput(format=('%Y-%m-%d'),attrs={'class':'form-control','type':'date','data-tooltip':"Fecha no puede ser superior al día de la fecha o fecha de vencimiento de permiso"}),
					help_text="Elija una nueva fecha y luego presione el boton de la calculadora para modificar el monto de Canon a cobrar.")

class PagoForm(forms.ModelForm):
	descripcion = forms.CharField(label='Descripción del Pago')
	archivo = forms.FileField(label='Adjuntar el Comprobante del Pago del Usuario')
	fecha = forms.DateField(label="Fecha de realizado el pago",widget=forms.DateInput(format=('%Y-%m-%d'),attrs={'class':'form-control','type':'date','data-tooltip':"Fijarse en el documento enviado por el solicitante, la fecha efectiva de pago"}))
	monto = forms.DecimalField(label='Ingreso el monto de pago')

	class Meta:
		model = Pago
		fields = ('descripcion', 'archivo', 'fecha','monto')