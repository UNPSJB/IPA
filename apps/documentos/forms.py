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

		fields = ['tipo','descripcion','archivo','fecha',]
		labels = {'tipo':'Tipo', 'descripcion':'Descripcion',
				'archivo':'Adjuntar el documento digital', 'fecha':'Fecha de entrega del documento',}

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
				'fecha': forms.DateInput(format=('%Y-%m-%d'),attrs={'type':'date'}),
		}

	def __init__(self,*args, **kwargs):
		super(DocumentoProtegidoForm,self).__init__(*args, **kwargs)
		#self.fields['fecha'].label = kwargs.get('initial')['texto']


class OposicionForm(forms.Form):
	valido = forms.ChoiceField(label='¿El reclamo del opositor es valido?', initial='False' ,choices=(('True', 'SI | Es valida la oposición, dar de BAJA el permiso'), ('False', 'NO | No es valida la oposición, continuar con los tramites del permiso'))) #'data-tooltip':"Seleccione esta casilla si la oposición es validad y poder así dar de baja el permiso."})

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
