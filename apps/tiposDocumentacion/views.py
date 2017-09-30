from django.shortcuts import render
from django.urls import reverse_lazy
from .models import TipoDocumentacion

# Create your views here.
def listar_tiposDocumentacion(request):
	botones = {
		"Listar" : 'documentos:listar',
		"Baja" : "#",
		"Alta" : "#", 
	}

	documentos = TipoDocumentacion.objects.all()

	headers = {'nombre':'nombre'}

	context = { 
		'headers': headers,
		'botones': botones,
		'documentos': documentos
	}
	
	return render(request, "lists.html", context)
