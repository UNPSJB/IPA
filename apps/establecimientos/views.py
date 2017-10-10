from django.shortcuts import render

from .models import Establecimiento
from .forms import EstablecimientoForm
from django.views.generic import CreateView, ListView

from django.core.urlresolvers import reverse_lazy


# Create your views here.
def alta_establecimiento(request):
	return render(request, 'establecimientos/altaEstablecimiento.html')


class AltaEstablecimiento(CreateView):
	model = Establecimiento
	form_class = EstablecimientoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('establecimientos:listar_establecimientos')


	def get_context_data(self, **kwargs):
		context = super(AltaEstablecimiento, self).get_context_data(**kwargs)
		context['botones'] = {'Alta': '/afluentes/alta_afluentes', 'Listado':'/afluentes/listar_afluentes'}
		context['nombreForm'] = 'Establecimientos'
		return context

class ListadoEstablecimientos(ListView):
	model = Establecimiento
	#form_class = AfluenteForm
	template_name = 'establecimientos/listado.html'
	context_object_name = 'establecimientos'

	def get_context_data(self, **kwargs):
		context = super(ListadoEstablecimientos, self).get_context_data(**kwargs)
		context['headers'] = ['Nombre', 'Localidad','Código Catastral']
		context['botones'] = {'Alta': '/establecimientos/alta_establecimiento', 'Listado':'/establecimientos/listar_establecimientos'}
		return context