from .forms import *

from django.core.urlresolvers import reverse_lazy

from .models import Afluente

from django.views.generic import ListView,CreateView,DeleteView,DetailView

class AltaAfluente(CreateView):
	model = Afluente
	form_class = AfluenteForm
	template_name = 'afluentes/altaAfluente.html'
	success_url = reverse_lazy('afluente:listar_afluentes')

class Detalle_Afluente(DetailView):
	model = Afluente
	template_name = 'afluentes/detalle_afluente.html'		


class ListadoAfluentes(ListView):
	model = Afluente
	#form_class = AfluenteForm
	template_name = 'afluentes/listado.html'
	context_object_name = 'afluentes'

	def get_context_data(self, **kwargs):
		context = super(ListadoAfluentes, self).get_context_data(**kwargs)
		context['headers'] = {'Nombre', 'Localidad','Caudal'}
		#context['botones'] = {'Alta': 'alta_afluentes', 'Listado':'listar_afluentes'}
		return context

class AfluenteDelete(DeleteView):
	model = Afluente
	template_name = 'afluentes/delete.html'
	success_url = reverse_lazy('afluente:listar_afluentes')