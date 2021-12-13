from django import forms
from .models import Comision
from ..personas.models import Persona
from django.forms.models import ModelMultipleChoiceField
from django.core.exceptions import ValidationError
from django.db.models import Q

class EmpModelChoiceField(ModelMultipleChoiceField):
	def label_from_instance(self, obj):
		return "{} {},{}".format(obj.getRolesParaComisionNames(), obj.apellido, obj.nombre)
		

class ComisionForm(forms.ModelForm):
	empleados = EmpModelChoiceField(label="Empleados", queryset=Persona.getEmpleadosParaComision(), required=True,
	widget=forms.SelectMultiple(attrs={'class':'form-control','id':'localidades','placeholder':'Ingrese el personal que hará el recorrido'}))
	
	class Meta:
		model = Comision

		fields = [
				#'empleados',
				'nota',
				'fechaInicio',
				'fechaFin',
				'motivo',
				'localidades',
		]
		
		labels = {
				'nota': 'Numero de Nota',
				'motivo': 'Motivo de la Comisión',
				'localidades':'Localidades',
				'fechaInicio':'Fecha de inicio',
				'fechaFin':'Fecha de finalizacion',
		}

		widgets = {
			#'empleados':forms.SelectMultiple(attrs={'class':'form-control','id':'empleados','placeholder':'Ingrese el personal que hará el recorrido'}),
			'nota': forms.TextInput(attrs={'class':'form-control','id':'nota','placeholder':'Ingresa el numero de nota por la cual se gestiona la comisión'}),
			'motivo': forms.Textarea(attrs={'class':'form-control','id':'motivo','placeholder':'Ingresa el motivo de la comisión'}),
			'localidades':forms.SelectMultiple(attrs={'class':'form-control','id':'localidades','placeholder':'Ingresa localidades a recorrer'}),
			'fechaInicio':forms.DateInput(format=('%Y-%m-%d'),attrs={'type':'date','id':'fechaInicio'}),
			'fechaFin':forms.DateInput(format=('%Y-%m-%d'),attrs={'type':'date','id':'fechaFin'}),
		}

		help_texts = {
			'': '',
		}
		
		error_messages = {
			'': {
				'max_length': "",
			},	
		}

	
	def clean(self):
		fecha_inicio = self.cleaned_data.get('fechaInicio')
		fecha_fin = self.cleaned_data.get('fechaFin')
		emp_comision = self.cleaned_data.get('empleados')
		validacion_fechas = Q(fechaInicio__range=(fecha_inicio,fecha_fin))|Q(fechaFin__range=(fecha_inicio,fecha_fin))|(Q(fechaInicio__lte=fecha_inicio)&Q(fechaFin__gte=fecha_inicio))
		comisiones = Comision.objects.filter(validacion_fechas&Q(empleados__in=emp_comision))

		if comisiones.exists():
			empleados_comprometidos = ''
			for e in comisiones.order_by('empleados__id').distinct('empleados__id').values_list('empleados__nombre','empleados__apellido'):
				empleados_comprometidos += e[0]+', '+e[1] + ' - '
			raise ValidationError("Los Empleados "+empleados_comprometidos[:-3]+" estan comprometidos en otras comisiones para el rango de fechas del "+
									fecha_inicio.strftime("%d-%m-%Y")+" al "+ fecha_fin.strftime("%d-%m-%Y"))

		if fecha_inicio>fecha_fin:
			raise ValidationError("La fecha de Inicio es mayor a la fecha de finalización")