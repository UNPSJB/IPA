from .forms import *

#from django.core.urlresolvers import reverse_lazy

from .models import Afluente

from django.views.generic import ListView,CreateView,DeleteView,UpdateView

class AltaAfluente(CreateView):
	model = Afluente
	form_class = AfluenteForm
	template_name = 'afluentes/altaAfluente.html'


class ListadoAfluentes(ListView):
	model = Afluente
	#form_class = AfluenteForm
	template_name = 'afluentes/listado.html'

	def get_context_data(self, **kwargs):
		context = super(ListadoAfluentes, self).get_context_data(**kwargs)
		context['headers'] = {'Nombre', 'Localidad','Caudal'}
		context['botones','url'] = {'Alta': 'alta_afluentes', 'Listado':'listar_afluentes'}
		return context

class AfluenteDelete(DeleteView):
	pass
	#model = Afluente
	#template_name = ''
	#success_url = reverse_lazy('xx:xx')