from django import forms
from .models import Permiso

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