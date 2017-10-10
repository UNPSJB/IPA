rom django.shortcuts import render

# Create your views here.
def alta_establecimiento(request):
	return render(request, 'establecimientos/altaEstablecimiento.html')