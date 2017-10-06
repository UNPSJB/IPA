from django.shortcuts import render

# Create your views here.

def alta_afluentes(request):
	return render(request, 'afluentes/altaAfluente.html')

def listar_afluentes(request):
	return render(request, 'afluentes/listado.html')