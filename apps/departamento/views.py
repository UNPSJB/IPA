from django.shortcuts import render

# Create your views here.
def alta_departamento(request):
	return render(request, 'departamento/altaDepartamento.html')