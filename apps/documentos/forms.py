from django import forms
from .models import TipoDocumento, Documento
from apps.comisiones.models import Comision
from apps.pagos.models import Pago
from django.core.exceptions import ValidationError
from datetime import date
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

	def clean_fecha(self):
		fecha_form = self.cleaned_data.get('fecha')

		if (fecha_form>date.today()):
			raise ValidationError("No es posible ingresar un documento nuevo con fecha mayor a la fecha actual ("+ fecha_form.today().strftime("%d-%m-%Y")+")")
		
		return fecha_form

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

	def clean_fecha(self):
		fecha_form = self.cleaned_data.get('fecha')

		if (fecha_form>date.today()):
			raise ValidationError("No es posible ingresar un documento nuevo con fecha mayor a la fecha actual ("+ fecha_form.today().strftime("%d-%m-%Y")+")")
		
		return fecha_form

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

		def clean_fecha(self):
			fecha_form = self.cleaned_data.get('fecha')
	
			if (fecha_form>date.today()):
				raise ValidationError("No es posible ingresar un documento nuevo con fecha mayor a la fecha actual ("+ fecha_form.today().strftime("%d-%m-%Y")+")")
			
			return fecha_form

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
				'fecha': forms.DateInput(attrs={'type':'date'},format=('%Y-%m-%d')),
		}

	def clean_fecha(self):
			fecha_form = self.cleaned_data.get('fecha')

			if (fecha_form>date.today()):
				raise ValidationError("No es posible ingresar un documento nuevo con fecha mayor a la fecha actual ("+ fecha_form.today().strftime("%d-%m-%Y")+")")
			
			return fecha_form

class ResolucionForm(forms.Form):
	unidad = forms.DecimalField(label='Unidad',max_digits=6,decimal_places=2, widget=forms.NumberInput(attrs={'class':'form-control','type':'number','min':'1','placeholder':'Ingrese la unidad del Permiso'}))
	#Fecha a partir de la cual se comienza a calcular el primer Cobro (Fecha de Solicitud de Permiso: 12 Dic. 2021 - Utilizando: No
	fechaPrimerCobro = forms.DateField(label="Fecha a partir de la cual se comienza a calcular el primer Cobro",widget=forms.DateInput(format=('%Y-%m-%d'),attrs={'class':'form-control','type':'date'}))
	fechaVencimiento = forms.DateField(label="Fecha de Vencimiento del Permiso",widget=forms.DateInput(format=('%Y-%m-%d'),attrs={'class':'form-control','type':'date'}))
	#unidad = forms.DecimalField(label='Unidad en KW')