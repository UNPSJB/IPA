from .forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .models import Modulo
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView

class AltaAModulo(CreateView):
	model = Modulo
	form_class = ModuloForm
	template_name = 'forms.html'
	success_url = reverse_lazy('modulo:listar')


	def get_context_data(self, **kwargs):
		context = super(AltaAModulo, self).get_context_data(**kwargs)
		context['botones'] = {'Alta': reverse('modulo:alta'), 'Listado': reverse('modulo:listar')}
		context['nombreForm'] = 'Modulo'
		return context

class DetalleModulo(DetailView):
	model = Modulo
	template_name = 'modulo/detalle.html'		


class ListadoModulo(ListView):
	model = Modulo
	template_name = 'modulo/listado.html'
	context_object_name = 'modulos'


	def get_context_data(self, **kwargs):
		context = super(ListadoModulo, self).get_context_data(**kwargs)
		context['nombreLista'] = 'Nombre'
		context['headers'] = ['Nombre', 'Codigo']
		context['botones'] = {'Alta': '/modulo/alta', 'Listado':'/modulo/listar'}
		return context

class ModificarModulo(UpdateView):
	model = Modulo
	form_class = ModuloForm
	template_name = 'modulo/form.html'
	success_url = reverse_lazy('modulo:listar')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_modulo = kwargs['pk']
		modulo = self.model.objects.get(id=id_modulo)
		form = self.form_class(request.POST, instance=modulo)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())


class DeleteModulo(DeleteView):
	model = Modulo
	template_name = 'modulo/delete.html'
	success_url = reverse_lazy('modulo:listar')