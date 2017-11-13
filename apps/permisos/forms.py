from django import forms
from .models import Permiso, TipoUso

class PermisoForm(forms.ModelForm):
    class Meta:
        model = Permiso

        fields = [
            'solicitante',
            'establecimiento',
            'tipo',
            'afluente',
            ]
        labels = {
            'solicitante' : 'Solicitante',
            'establecimiento' : 'Establecimiento',
            'tipo' : 'Tipo',
            'afluente' : 'Afluente',
            }

        widgets = {
            'solicitante':forms.Select(attrs={'class':'form-control'}),
            'establecimiento':forms.Select(attrs={'class':'form-control'}),
            'tipo':forms.Select(attrs={'class':'form-control'}),
            'afluente':forms.Select(attrs={'class':'form-control'}),
            }


class TipoDeUsoForm(forms.ModelForm):
    class Meta:
        model = TipoUso

        fields = [
                'descripcion',
                'coeficiente',
                'periodo',
                'medida',
                'tipo_modulo',
          #      'documentos',
            ]
        labels = {
                'descripcion': 'Descripcion',
                'coeficiente': 'Coeficiente',
                'periodo': 'Periodo',
                'medida': 'Medida',
                'tipo_modulo': 'Tipo modulo',
         #       'documentos': 'Documentos',
        }

        widgets = {
            'descripcion':forms.TextInput(attrs={'class':'form-control'}),
            'coeficiente':forms.TextInput(attrs={'class':'form-control'}),
            'periodo':forms.Select(attrs={'class':'form-control'}),
            'medida':forms.Select(attrs={'class':'form-control'}),
            'tipo_modulo':forms.Select(attrs={'class':'form-control'}),
        #    'documentos':forms.SelectMultiple(attrs={'class':'form-control'}),
        }