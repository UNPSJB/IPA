from django import forms
from .models import TipoDocumento, Documento
from apps.comisiones.models import Comision
from apps.pagos.models import Pago
from django.core.exceptions import ValidationError

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

		fields = ['tipo','descripcion','archivo','fecha',]
		labels = {'tipo':'Tipo', 'descripcion':'Descripcion',
				'archivo':'Adjuntar el documento digital', 'fecha':'Fecha de entrega del documento',}

		widgets = {
				'tipo':forms.Select(attrs={'class':'form-control'}),
				'descripcion':forms.TextInput(attrs={'class':'form-control'}),
				'fecha': forms.DateInput(format=('%Y-%m-%d'),attrs={'type':'date'}),
		}

class ModificarDocumentoForm(DocumentoForm):
	documento_nuevo = forms.ChoiceField(label='¿Es un Nuevo Documento?', initial='False', widget=forms.Select(attrs={'id':'documento_nuevo'}), choices=(('True', 'SI | Es un nuevo documento entregado por el usuario'), ('False', 'NO | Solamente es la modificación de datos previamente cargados')))

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
				'fecha': forms.DateInput(format=('%Y-%m-%d'),attrs={'type':'date'}),
		}

	def __init__(self,*args, **kwargs):
		super(DocumentoProtegidoForm,self).__init__(*args, **kwargs)

class OposicionForm(forms.Form):
	valido = forms.ChoiceField(label='¿El reclamo del opositor es valido?', initial='False' ,choices=(('True', 'SI | Es valida la oposición, dar de BAJA el permiso'), ('False', 'NO | No es valida la oposición, continuar con los tramites del permiso')))

class DocumentoActaInspeccionProtegidoForm(forms.ModelForm):
	comision = forms.ModelChoiceField(label='Ingrese la comisión en donde se genero el acta',queryset=Comision.objects.all())
	
	class Meta:
		model = Documento

		fields = [
				'descripcion',
				'archivo',
				'fecha',
			]
			
		labels = {
				'descripcion':'Descripcion',
				'archivo':'Documento del Acta de Inspección',
				'fecha':'Fecha del Acta',
		}

		widgets = {
				'descripcion':forms.TextInput(attrs={'class':'form-control'}),
				'fecha': forms.DateInput(attrs={'type':'date'}),
		}

class DocumentoActaInsfraccionProtegidoForm(forms.ModelForm):
	comision = forms.ModelChoiceField(label='Ingrese la comisión en donde se genero el acta', queryset=Comision.objects.all())
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
				'archivo':'Documento del Acta de Infracción',
				'fecha':'Fecha del Acta',
				'comision': 'Ingrese la comisión en donde se genero el acta'
		}

		widgets = {
				'descripcion':forms.TextInput(attrs={'class':'form-control'}),
				'fecha': forms.DateInput(attrs={'type':'date'}),
		}

