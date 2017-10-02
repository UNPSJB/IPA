from django.shortcuts import render

# Create your views here.

def listarSolicitudes(request):
	botones = {
		"Listar" : 'permisos:listarSolicitudes',
		"Baja" : "#",
		"Alta" : "#", 
	}

	documentos = Solicitud.objects.all()

	headers = {'nombre':'nombre'}

	context = { 
		'headers': headers,
		'botones': botones,
		'documentos': documentos
	}
	
	return render(request, "lists.html", context)

