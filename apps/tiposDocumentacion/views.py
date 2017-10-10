from django.shortcuts import render
from django.urls import reverse_lazy
from .models import TipoDocumentacion
from .forms import AltaForm

# Create your views here.
def listar_tiposDocumentacion(request):
	botones = {
		"Listar" : '/documentos/listar',
		"Alta" : "/documentos/alta",
	}

	documentos = TipoDocumentacion.objects.all()

	headers = ['Nombre']

	context = { 
		"nombreLista": 'Tipos de Documento',
		'headers': headers,
		'botones': botones,
		'documentos': documentos
	}
	
	return render(request, "listar.html", context)

def alta_tiposDocumentos(request):
	botones = {
		"Listar" : 'documentos:listar',
		"Alta" : "documentos:Alta", 
	}

	altaForm = AltaForm(request.POST or None)

	context = { 
		"nombreLista": "Tipos de Documento",
		"form": altaForm,
		"botones": botones
	}

	if request.POST and form.is_valid():
		pass # Do whatever

	return render(request, "forms.html", context)