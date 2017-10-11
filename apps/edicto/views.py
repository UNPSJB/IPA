from .forms import *

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Edicto

from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView

class AltaEdicto(CreateView):
	model = Edicto
	form_class = EdictoForm
	template_name = 'forms.html'
	success_url = reverse_lazy('edicto:listar_edicto')


	def get_context_data(self, **kwargs):
		context = super(AltaEdicto, self).get_context_data(**kwargs)
		context['botones'] = {'Alta': '/edicto/alta_edicto', 'Listado':'/edito/listar_edicto'}
		context['nombreForm'] = 'Edicto'
		return context

class Detalle_Edicto(DetailView):
	model = Edicto
	template_name = 'edicto/detalle_edicto.html'		


class ListadoEdictos(ListView):
	model = Edicto
	#form_class = AfluenteForm
	template_name = 'edicto/listado.html'
	context_object_name = 'edictos'

	def get_context_data(self, **kwargs):
		context = super(ListadoEdictos, self).get_context_data(**kwargs)
		context['headers'] = ['Numero', 'Fecha Publicacion','Fecha Exigencia']
		context['botones'] = {'Alta': '/edictos/alta_edictos', 'Listado':'/edictos/listar_edictos'}
		return context

class ModificarEdicto(UpdateView):
	model = Edicto
	form_class = EdictoForm
	template_name = 'edicto/form.html'
	success_url = reverse_lazy('edictos:listar_edictos')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_afluente = kwargs['pk']
		afluente = self.model.objects.get(id=id_edicto)
		form = self.form_class(request.POST, instance=edicto)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())


class EdictoDelete(DeleteView):
	model = Edicto
	template_name = 'edicto/delete.html'
	success_url = reverse_lazy('edictos:listar_edictos')