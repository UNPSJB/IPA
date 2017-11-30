from django import forms
from .models import TipoDocumento, Documento
from apps.comisiones.models import Comision
from apps.pagos.models import Pago

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
			'nombre':forms.TextInput(attrs={'class':'form-control', 'placehorder':'Nombre del Documento'}),
	
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
				'fecha':'Fecha del Documento',
		}

		widgets = {
				'tipo':forms.Select(attrs={'class':'form-control'}),
				'descripcion':forms.TextInput(attrs={'class':'form-control'}),
				'fecha': forms.DateInput(attrs={'type':'date'}),
		}


class DocumentoProtegidoForm(forms.ModelForm):
	class Meta:
		model = Documento

		fields = [
				'descripcion',
				'archivo',
				'fecha',
			]
		labels = {
				'descripcion':'Descripcion',
				'archivo':'Archivo',
				'fecha':'Fecha del Documento',
		}

		widgets = {
				'descripcion':forms.TextInput(attrs={'class':'form-control'}),
				'fecha': forms.DateInput(attrs={'type':'date'}),
		}

class DocumentoActaInspeccionProtegidoForm(forms.ModelForm):
	comision = forms.ModelChoiceField(queryset=Comision.objects.all())
	
	class Meta:
		model = Documento

		fields = [
				'descripcion',
				'archivo',
				'fecha',
				'comision'
			]
			
		labels = {
				'descripcion':'Descripcion',
				'archivo':'Archivo',
				'fecha':'Fecha del Documento',
		}

		widgets = {
				'descripcion':forms.TextInput(attrs={'class':'form-control'}),
				'fecha': forms.DateInput(attrs={'type':'date'}),
		}


class DocumentoActaInsfraccionProtegidoForm(forms.ModelForm):
	comision = forms.ModelChoiceField(queryset=Comision.objects.all())
	pago = forms.ModelChoiceField(queryset=Pago.objects.all())
	
	class Meta:
		model = Documento

		fields = [
				'descripcion',
				'archivo',
				'fecha',
				'comision'
			]
			
		labels = {
				'descripcion':'Descripcion',
				'archivo':'Archivo',
				'fecha':'Fecha del Documento',
		}

		widgets = {
				'descripcion':forms.TextInput(attrs={'class':'form-control'}),
				'fecha': forms.DateInput(attrs={'type':'date'}),
		}
