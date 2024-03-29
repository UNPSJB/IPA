from django import forms
from apps.permisos.models import TipoUso
from apps.establecimientos.models import *

class FiltroForm(forms.Form):

    tipos_permisos = forms.ModelMultipleChoiceField(label="Tipos de Permisos",queryset=None,required=False)
    afluentes = forms.ModelMultipleChoiceField(label="Afluentes utilizados", queryset=None,to_field_name="pk",required=False)
    localidades = forms.ModelMultipleChoiceField(label="Localidades de los Establecimientos",queryset=None,to_field_name="pk",required=False)
    departamentos = forms.ModelMultipleChoiceField(label="Departamentos de los Establecimientos", queryset=None,to_field_name="pk",required=False)

    def __init__(self, *args, **kwargs):
        super(FiltroForm, self).__init__(*args,**kwargs)
        self.fields['tipos_permisos'].queryset = TipoUso.objects.all()
        self.fields['afluentes'].queryset = Afluente.objects.all()
        self.fields['localidades'].queryset = Localidad.objects.all()
        self.fields['departamentos'].queryset = Departamento.objects.all()

class FiltroRecaudacionForm(FiltroForm):
    OPERACION = [
        ("Cobro","Cobro"),
        ("Pago","Pago"),
    ]

    MOTIVO = [
        (True,'Canon'),
        (False,'Infracción')
    ]

    operaciones = forms.ChoiceField(label="Operación",choices=OPERACION,required=False,widget=forms.Select(attrs={'class':'form-control','id':'filtro_operaciones'}))
    motivos = forms.ChoiceField(label="Motivo de Operación",choices=MOTIVO,required=False,widget=forms.Select(attrs={'class':'form-control','id':'filtro_motivos'}))

    field_order = ['tipos_permisos', 'operaciones', 'motivos','afluentes','localidades','departamentos']