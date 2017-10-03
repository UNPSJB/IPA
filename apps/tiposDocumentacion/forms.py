from django import forms
from .models import TipoDocumentacion

class AltaForm(forms.Form):
	name = forms.CharField(max_length=50, help_text="Nombre de documentacion")
	

