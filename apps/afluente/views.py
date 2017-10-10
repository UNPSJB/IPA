from .forms import *

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Afluente

from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView

class AltaAfluente(CreateView):
	model = Afluente
	form_class = AfluenteForm
	template_name = 'forms.html'
	success_url = reverse_lazy('afluente:listar_afluentes')


	def get_context_data(self, **kwargs):
		context = super(AltaAfluente, self).get_context_data(**kwargs)
		context['botones'] = {'Alta': '/afluentes/alta_afluentes', 'Listado':'/afluentes/listar_afluentes'}
		return context

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
		context['headers'] = ['Nombre', 'Localidad','Caudal']
		context['botones'] = {'Alta': '/afluentes/alta_afluentes', 'Listado':'/afluentes/listar_afluentes'}
		return context

class ModificarAfluente(UpdateView):
	model = Afluente
	form_class = AfluenteForm
	template_name = 'afluentes/form.html'
	success_url = reverse_lazy('afluentes:listar_afluentes')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_afluente = kwargs['pk']
		afluente = self.model.objects.get(id=id_afluente)
		form = self.form_class(request.POST, instance=afluente)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())


class AfluenteDelete(DeleteView):
	model = Afluente
	template_name = 'afluentes/delete.html'
	success_url = reverse_lazy('afluente:listar_afluentes')