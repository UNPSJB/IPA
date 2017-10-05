from django.shortcuts import render

# Create your views here.

def alta_afluente(request):
	return render(request, 'afluentes/altaAfluente.html')