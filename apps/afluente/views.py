from django.shortcuts import render

from .models import Afluente

# Create your views here.

def alta_afluentes(request):
	return render(request, 'afluentes/altaAfluente.html')

def listar_afluentes(request):
	botones = {
		"Listar": "#",
		"Baja": "#",
		"Alta": "#", 
	}

	afluentes = Afluente.objects.all()

	headers = {'nombre':'nombre'}

	context = { 
		'headers': headers,
		'botones': botones,
		'afluentes': afluentes,
	}
	
	return render(request, 'afluentes/listado.html', context)